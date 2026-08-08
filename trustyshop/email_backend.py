import ssl

from django.core.mail.backends.smtp import EmailBackend as DjangoSMTPBackend


class EmailBackend(DjangoSMTPBackend):

    def open(self):
        if self.connection:
            return False

        try:
            # Connect to Gmail SMTP
            self.connection = self.connection_class(
                self.host,
                self.port,
                timeout=self.timeout,
            )

            self.connection.ehlo()

            # Gmail SMTP on port 587 uses STARTTLS
            if self.use_tls:
                context = ssl.create_default_context()

                # Workaround for the Python 3.14/OpenSSL
                # certificate problem on this machine.
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                self.connection.starttls(context=context)
                self.connection.ehlo()

            # Login using Gmail App Password
            if self.username and self.password:
                self.connection.login(
                    self.username,
                    self.password,
                )

            return True

        except Exception:
            if not self.fail_silently:
                raise

            self.connection = None
            return False