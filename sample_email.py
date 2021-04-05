
import argparse
import getpass
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


HTML_BODY = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <title>DataDev Day 2021</title>
    <meta content="width=device-width" name="viewport">
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <style type="text/css">
        /* CLIENT-SPECIFIC STYLES */

        #outlook a {
            padding: 0;
        }
        /* Force Outlook to provide a "view in browser" message */

        .ReadMsgBody {
            width: 100%;
        }

        .ExternalClass {
            width: 100%;
        }
        /* Force Hotmail to display emails at full width */

        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {
            line-height: 100%;
        }
        /* Force Hotmail to display normal line spacing */

        body,
        table,
        td,
        a {{
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }}
        /* Prevent WebKit and Windows mobile changing default text sizes */

        table,
        td {
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }
        /* Remove spacing between tables in Outlook 1957 and up */

        img {
            -ms-interpolation-mode: bicubic;
        }
        /* Allow smoother rendering of resized image in Internet Explorer */
        /* RESET STYLES */

        body {
            margin: 0;
            padding: 0;
        }

        img {
            border: 0;
            line-height: 100%;
            outline: none;
            text-decoration: none;
        }

        table {
            border-collapse: collapse !important;
        }

        body {
            height: 100% !important;
            margin: 0;
            padding: 0;
            width: 100% !important;
        }

        @media screen and (max-width: 600px) {
            table[class="wrapper"] {{
                width: 100% !important;
            }
            td[class="logo"] {
                text-align: left;
                padding: 20px 0 20px 0 !important;
            }
            td[class="mobile-hide"] {
                display: none !important;
            }
            td[class="logo"] img {
                margin: 0 auto!important;
            }
            img[class="img-max"] {
                max-width: 100%;
                height: auto;
            }
            table[class=body] .btn table {
                width: 100% !important;
            }
            table[class="responsive-table"] {
                width: 100%!important;
            }
            td[class="section-padding"] {
                padding: 30px 15px 0px 15px !important;
            }
            td[class="section-padding2"] {
                padding: 30px 15px 0 15px !important;
            }
        }
    </style>
</head>
<body style="margin: 0; padding: 0;">
<!-- HEADER -->
<table border="0" cellpadding="0" cellspacing="0" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="100%">
    <tr>
        <td align="center" bgcolor="#FFFFFF" class="section-padding" style="padding-top:10px;padding-bottom:10px;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
            <table border="0" cellpadding="0" cellspacing="0" class="responsive-table" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="500">
                <tr>
                    <td style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                        <table border="0" cellpadding="0" cellspacing="0" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="100%">
                            <tr>
                                <td style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                                    <table border="0" cellpadding="0" cellspacing="0" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="100%">
                                        <tbody>
                                        <tr>
                                            <td style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                                                <table border="0" cellpadding="0" cellspacing="0" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="100%">
                                                    <tr>
                                                        <td align="center" bgcolor="#FFFFFF" width="215">
                                                            <a href="https://www.tableau.com/DataDevDay"><img src="http://mkt.tableausoftware.com/emails/template/i/tableau_cmyk.png" style="display: block;" width="215"></a>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table><!--Hero Grid-->
<table border="0" cellpadding="0" cellspacing="0" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="100%">
    <tr>
        <td align="center" bgcolor="#FFFFFF" class="section-padding" style="padding-top:10px;padding-bottom:10px;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
            <table border="0" cellpadding="0" cellspacing="0" class="responsive-table" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="600">
                <tr>
                    <td style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                        <table border="0" cellpadding="0" cellspacing="0" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="100%">
                            <tr>
                                <td style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                                    <!-- Text Grid -->
                                    <table border="0" cellpadding="0" cellspacing="0" style="-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse !important;" width="100%">
                                        <tr>
                                            <td align="center" style="font-size:24px;font-family: Benton Sans, sans-serif;color:#666666;padding-top:30px;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                                                DataDev Day 2021
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="padding-top:5px;padding-bottom:0;padding-right:0;padding-left:0;font-size:18px;line-height:25px;font-family: Benton Sans, sans-serif;color:#666666;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                                                From an API Call to an Enterprise Application
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="font-size:14px;font-family: Benton Sans, sans-serif;color:#666666;padding-top:30px;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;mso-table-lspace:0pt;mso-table-rspace:0pt;">
                                                Python sent this email!                               
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>
</html>
"""


def main():

    parser = argparse.ArgumentParser(description="Send Email using Python")
    parser.add_argument('--server', '-s', required=True, help='smtp server')
    parser.add_argument('--port', '-p', required=False, default=25, help='smtp server port')
    parser.add_argument('--user', '-u', required=False, help='user for smtp authentication')
    parser.add_argument('--sender', '-e', required=True, help='email address of sender (FROM)')
    parser.add_argument('--recipient', '-r', required=True, help='email address of recipient (TO)')

    args = parser.parse_args()
    password = None

    if args.user:
        password = getpass.getpass(f'{args.user} Password: ')

    msg = MIMEMultipart('related')
    msg['Subject'] = "Tableau DataDev Day 2021 Test Email"
    msg['From'] = args.sender
    msg['To'] = args.recipient

    email_body = MIMEText(HTML_BODY, 'html')
    msg.attach(email_body)

    smtp = smtplib.SMTP(args.server, args.port)

    if args.user:
        smtp.login(args.user, password)

    try:
        smtp.sendmail(args.sender, args.recipient, msg.as_string())
    except smtplib.SMTPException as e:
        print(e)
    finally:
        smtp.quit()


if __name__ == '__main__':
    main()
