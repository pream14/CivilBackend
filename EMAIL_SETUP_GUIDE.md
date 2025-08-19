# Email Setup Guide - SendGrid Configuration

## Why You're Not Receiving Emails

The email notification feature is implemented but you're not receiving emails because **SendGrid is not configured yet**. Here's how to fix this:

## Step-by-Step Setup

### 1. Create SendGrid Account (Free)

1. **Sign up**: Go to [sendgrid.com](https://sendgrid.com) and create a free account
2. **Verify email**: Confirm your email address
3. **Complete setup**: Follow the onboarding process

### 2. Get Your API Key

1. **Login** to SendGrid dashboard
2. **Go to Settings** → **API Keys**
3. **Create API Key**:
   - Click "Create API Key"
   - Name: `Civil Backend Email`
   - Permissions: Select **"Mail Send"** (Full Access)
   - Click "Create & View"
4. **Copy the API Key** (it starts with `SG.`)

### 3. Verify Sender Email

1. **Go to Settings** → **Sender Authentication**
2. **Choose option**:
   - **Option A**: Verify Single Sender (easier)
   - **Option B**: Verify Domain (more professional)
3. **For Single Sender**:
   - Click "Verify a Single Sender"
   - Fill in your details
   - Use your real email (e.g., `yourname@gmail.com`)
   - Click "Create"
   - Check your email and click the verification link

### 4. Update Your .env File

Edit the file `CivilBackend/.env`:

```env
# Email Configuration
SENDGRID_API_KEY=SG.your_actual_api_key_here
FROM_EMAIL=your_verified_email@gmail.com
TO_EMAIL=22z269@psgtech.ac.in
```

**Replace**:
- `SG.your_actual_api_key_here` with your actual SendGrid API key
- `your_verified_email@gmail.com` with your verified sender email

### 5. Test Email Configuration

1. **Restart your Flask server**
2. **Test the email endpoint**:
   ```
   GET http://10.1.226.6:5000/test-email
   ```
3. **Check the response** to see if configuration is correct

### 6. Test with Real Data

1. **Add an expense** that triggers budget overrun
2. **Check your email** at `22z269@psgtech.ac.in`
3. **Check console logs** for email status

## Troubleshooting

### Common Issues

1. **"API key not configured" error**:
   - Make sure you updated the `.env` file
   - Restart your Flask server after updating `.env`

2. **"Authentication failed" error**:
   - Check your API key is correct
   - Ensure API key has "Mail Send" permissions

3. **"Sender not verified" error**:
   - Verify your sender email in SendGrid
   - Use the exact same email in `FROM_EMAIL`

4. **Email not received**:
   - Check spam/junk folder
   - Verify recipient email is correct
   - Check SendGrid Activity logs

### Quick Test Without SendGrid

If you want to test the system without setting up SendGrid:

1. **Use dummy API key** in `.env`:
   ```env
   SENDGRID_API_KEY=dummy_key
   ```

2. **System will work normally** but emails will fail gracefully
3. **Check console logs** to see email attempts

## Alternative: Use Gmail SMTP (Free)

If you prefer not to use SendGrid, you can use Gmail SMTP:

1. **Enable 2-factor authentication** on your Gmail
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Update .env**:
   ```env
   EMAIL_PROVIDER=gmail
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASSWORD=your_app_password
   ```

## Security Notes

- ✅ **Never commit API keys** to version control
- ✅ **Use .env file** for sensitive data
- ✅ **Keep API keys private**
- ✅ **Rotate keys regularly**

## Next Steps

After setup:
1. Test with small expenses first
2. Monitor email delivery
3. Check SendGrid dashboard for delivery stats
4. Consider upgrading to paid plan for higher limits

## Support

If you need help:
1. Check SendGrid documentation
2. Review console logs for errors
3. Test with the `/test-email` endpoint
4. Verify all configuration steps 