/*
 * Copyright (C) 2009-2012 Red Hat, Inc.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General
 * Public License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place, Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 * Author: David Zeuthen <davidz@redhat.com>
 */

#ifdef HAVE_CONFIG_H
#  include "config.h"
#endif

#include <stdio.h>
#include <glib/gi18n.h>
#include <polkit/polkit.h>
#define POLKIT_AGENT_I_KNOW_API_IS_SUBJECT_TO_CHANGE
#include <polkitagent/polkitagent.h>

int
main (int argc, char *argv[])
{
  gboolean opt_show_version = FALSE;
  gboolean opt_fallback = FALSE;
  gchar *opt_process = NULL;
  gchar *opt_system_bus_name = NULL;
  gint opt_notify_fd = -1;
  GOptionEntry options[] =
    {
      {
	"fallback", 0, 0, G_OPTION_ARG_NONE, &opt_fallback,
	N_("Don't replace existing agent if any"), NULL
      },
      {
	"notify-fd", 0, 0, G_OPTION_ARG_INT, &opt_notify_fd,
	N_("Close FD when the agent is registered"), N_("FD")
      },
      {
	"process", 'p', 0, G_OPTION_ARG_STRING, &opt_process,
	N_("Register the agent for the specified process"),
	N_("PID[,START_TIME]")
      },
      {
	"system-bus-name", 's', 0, G_OPTION_ARG_STRING, &opt_system_bus_name,
	N_("Register the agent owner of BUS_NAME"), N_("BUS_NAME")
      },
      {
	"version", 0, 0, G_OPTION_ARG_NONE, &opt_show_version,
	N_("Show version"), NULL
      },
      { NULL, 0, 0, 0, NULL, NULL, NULL }
    };
  GOptionContext *context;
  gchar *s;
  PolkitAuthority *authority = NULL;
  PolkitSubject *subject = NULL;
  gpointer local_agent_handle = NULL;
  PolkitAgentListener *listener = NULL;
  GVariant *listener_options = NULL;
  GError *error;
  GMainLoop *loop = NULL;
  guint ret = 126;
  GVariantBuilder builder;

  g_type_init ();

  error = NULL;
  context = g_option_context_new ("");
  s = g_strdup_printf (_("Report bugs to: %s\n"
			 "%s home page: <%s>"), PACKAGE_BUGREPORT,
		       PACKAGE_NAME, PACKAGE_URL);
  g_option_context_set_description (context, s);
  g_free (s);
  g_option_context_add_main_entries (context, options, GETTEXT_PACKAGE);
  if (!g_option_context_parse (context, &argc, &argv, &error))
    {
      g_printerr ("%s: %s\n", g_get_prgname (), error->message);
      g_error_free (error);
      goto out;
    }
  if (argc > 1)
    {
      g_printerr (_("%s: Unexpected argument `%s'\n"), g_get_prgname (),
		  argv[1]);
      goto out;
    }

  if (opt_show_version)
    {
      g_print ("pkttyagent version %s\n", PACKAGE_VERSION);
      ret = 0;
      goto out;
    }

  if (opt_process != NULL)
    {
      gint pid;
      guint64 pid_start_time;

      if (sscanf (opt_process, "%i,%" G_GUINT64_FORMAT, &pid, &pid_start_time)
	  == 2)
	subject = polkit_unix_process_new_full (pid, pid_start_time);
      else if (sscanf (opt_process, "%i", &pid) == 1)
	subject = polkit_unix_process_new (pid);
      else
	{
	  g_printerr (_("%s: Invalid process specifier `%s'\n"),
		      g_get_prgname (), opt_process);
	  goto out;
	}
    }
  if (opt_system_bus_name != NULL)
    subject = polkit_system_bus_name_new (opt_system_bus_name);
  /* Use parent process, if no subject has been specified */
  if (subject == NULL)
    {
      pid_t pid_of_caller;
      pid_of_caller = getppid ();
      if (pid_of_caller == 1)
        {
          /* getppid() can return 1 if the parent died (meaning that we are reaped
           * by /sbin/init); In that case we simpy bail.
           */
          g_printerr ("Refusing to render service to dead parents.\n");
          goto out;
        }

      subject = polkit_unix_process_new_for_owner (pid_of_caller,
                                                   0, /* 0 means "look up start-time in /proc" */
                                                   getuid ());
      /* really double-check the invariants guaranteed by the PolkitUnixProcess class */
      g_assert (subject != NULL);
      g_assert (polkit_unix_process_get_pid (POLKIT_UNIX_PROCESS (subject)) == pid_of_caller);
      g_assert (polkit_unix_process_get_uid (POLKIT_UNIX_PROCESS (subject)) >= 0);
      g_assert (polkit_unix_process_get_start_time (POLKIT_UNIX_PROCESS (subject)) > 0);
    }

  authority = polkit_authority_get_sync (NULL /* GCancellable* */, &error);
  if (authority == NULL)
    {
      g_printerr ("Error getting authority: %s (%s, %d)\n",
                  error->message, g_quark_to_string (error->domain), error->code);
      g_error_free (error);
      ret = 127;
      goto out;
    }

  if (opt_fallback)
    {
      g_variant_builder_init (&builder, G_VARIANT_TYPE_VARDICT);
      g_variant_builder_add (&builder, "{sv}", "fallback", g_variant_new_boolean (TRUE));
      listener_options = g_variant_builder_end (&builder);
    }

  error = NULL;
  /* this will fail if we can't find a controlling terminal */
  listener = polkit_agent_text_listener_new (NULL, &error);
  if (listener == NULL)
    {
      g_printerr ("Error creating textual authentication agent: %s (%s, %d)\n",
                  error->message, g_quark_to_string (error->domain), error->code);
      g_error_free (error);
      ret = 127;
      goto out;
    }
  local_agent_handle = polkit_agent_listener_register_with_options (listener,
                                                                    POLKIT_AGENT_REGISTER_FLAGS_RUN_IN_THREAD,
                                                                    subject,
                                                                    NULL, /* object_path */
                                                                    listener_options,
                                                                    NULL, /* GCancellable */
                                                                    &error);
  listener_options = NULL; /* consumed */
  g_object_unref (listener);
  if (local_agent_handle == NULL)
    {
      g_printerr ("Error registering authentication agent: %s (%s, %d)\n",
                  error->message, g_quark_to_string (error->domain), error->code);
      g_error_free (error);
      goto out;
    }

  if (opt_notify_fd != -1)
    {
      if (close (opt_notify_fd) != 0)
        {
          g_printerr ("Error closing notify-fd %d: %m\n", opt_notify_fd);
          goto out;
        }
    }

  loop = g_main_loop_new (NULL, FALSE);
  g_main_loop_run (loop);

 out:
  if (loop != NULL)
    g_main_loop_unref (loop);

  if (local_agent_handle != NULL)
    polkit_agent_listener_unregister (local_agent_handle);

  if (listener_options != NULL)
    g_variant_unref (listener_options);

  if (subject != NULL)
    g_object_unref (subject);

  if (authority != NULL)
    g_object_unref (authority);

  g_free (opt_process);
  g_free (opt_system_bus_name);
  g_option_context_free (context);

  return ret;
}
