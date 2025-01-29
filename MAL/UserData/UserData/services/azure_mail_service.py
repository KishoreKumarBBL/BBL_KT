from azure.communication.email import EmailClient

from bugbusterslabs import settings

POLLER_WAIT_TIME = 10


def send_azure_mail(subject, html_body, from_email, to_email):
    try:
        connection_string = settings.AZURE_MAIL_URL
        email_client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": from_email,
            "recipients": {
                "to": [{"address": to_email}],
            },
            "content": {"subject": subject, "html": html_body, "plainText": html_body},
        }

        poller = email_client.begin_send(message)

        time_elapsed = 0
        while not poller.done():
            print("Email send poller status: " + poller.status())

            poller.wait(POLLER_WAIT_TIME)
            time_elapsed += POLLER_WAIT_TIME

            if time_elapsed > 18 * POLLER_WAIT_TIME:
                raise RuntimeError("Polling timed out.")

        if poller.result()["status"] == "Succeeded":
            print(
                f"Successfully sent the email (operation id: {poller.result()['id']})"
            )
        else:
            raise RuntimeError(str(poller.result()["error"]))

    except Exception as ex:
        raise Exception("Failed to send mail using Azure: " + str(ex))


def send_multi_azure_mail(subject, html_body, from_email, to_emails):
    try:
        connection_string = settings.AZURE_MAIL_URL
        email_client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": from_email,
            "recipients": {
                "to": [{"address": email} for email in to_emails],
            },
            "content": {"subject": subject, "html": html_body, "plainText": html_body},
        }

        poller = email_client.begin_send(message)

        time_elapsed = 0
        while not poller.done():
            print("Email send poller status: " + poller.status())

            poller.wait(POLLER_WAIT_TIME)
            time_elapsed += POLLER_WAIT_TIME

            if time_elapsed > 18 * POLLER_WAIT_TIME:
                raise RuntimeError("Polling timed out.")

        if poller.result()["status"] == "Succeeded":
            print(
                f"Successfully sent the email (operation id: {poller.result()['id']})"
            )
        else:
            raise RuntimeError(str(poller.result()["error"]))

    except Exception as ex:
        raise Exception("Failed to send mail using Azure: " + str(ex))
