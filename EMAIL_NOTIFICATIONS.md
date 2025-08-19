# Email Notifications for Budget Overruns

## Overview

The system automatically sends email notifications when a project's predicted final cost exceeds its quoted budget. This feature provides timely alerts to project managers and stakeholders, complementing the in-app budget overrun warnings.

## Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Email Configuration
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=noreply@yourdomain.com
TO_EMAIL=22z269@psgtech.ac.in
```

### SendGrid Setup

1. **Create SendGrid Account**: Sign up at [sendgrid.com](https://sendgrid.com)
2. **Get API Key**: 
   - Go to Settings → API Keys
   - Create a new API Key with "Mail Send" permissions
   - Copy the API key to your `.env` file
3. **Verify Sender Email**:
   - Go to Settings → Sender Authentication
   - Verify your domain or single sender email
   - Update `FROM_EMAIL` in your `.env` file

## How It Works

### Trigger Points

Email notifications are sent automatically when:

1. **Expense Addition**: When a new expense is added via `/add_expense` endpoint
2. **Manual Check**: When budget overrun is checked via `/check-overrun` endpoint

### Email Content

The email includes:

- **Project Details**: Name, quoted budget, predicted cost
- **Budget Variance**: Amount and percentage over budget
- **Recommended Actions**: List of suggested cost control measures
- **Professional Styling**: HTML email with responsive design

### Email Recipients

- **Default**: `22z269@psgtech.ac.in` (as specified in requirements)
- **Configurable**: Can be changed via `TO_EMAIL` environment variable
- **Future Enhancement**: Support for multiple recipients and dynamic project-specific emails

## Email Template

The email uses a professional HTML template with:

- **Header**: Clear "Budget Overrun Alert" title
- **Alert Box**: Attention-grabbing warning message
- **Metrics**: Key financial data in organized sections
- **Action Items**: Recommended steps to address the overrun
- **Footer**: System information and timestamp

## Error Handling

- **Graceful Degradation**: If email sending fails, the expense addition still succeeds
- **Logging**: All email attempts are logged to console
- **Fallback**: System continues to function even if email service is unavailable

## Testing

### Test Email Sending

1. **Set up SendGrid**: Follow the configuration steps above
2. **Add Test Expense**: Add an expense that triggers budget overrun
3. **Check Email**: Verify email is received at the configured address
4. **Check Logs**: Review console output for email status

### Test Without SendGrid

If you don't want to set up SendGrid immediately:

1. **Use Dummy API Key**: Set `SENDGRID_API_KEY=dummy_key` in `.env`
2. **Check Logs**: Email attempts will fail but be logged
3. **System Continues**: All other functionality remains intact

## Security Considerations

- **API Key Protection**: Never commit API keys to version control
- **Environment Variables**: Use `.env` file for sensitive configuration
- **Email Validation**: SendGrid validates sender email addresses
- **Rate Limiting**: SendGrid has built-in rate limiting

## Future Enhancements

### Planned Features

1. **Multiple Recipients**: Support for project-specific email lists
2. **Email Templates**: Customizable email content and styling
3. **Scheduled Reports**: Periodic budget status emails
4. **Escalation Rules**: Different notification levels based on overrun severity
5. **Email Preferences**: User-configurable notification settings

### Integration Possibilities

- **Slack Integration**: Send notifications to Slack channels
- **SMS Alerts**: Text message notifications for critical overruns
- **Dashboard Alerts**: Real-time notifications in web dashboard
- **Mobile Push**: Push notifications in mobile app

## Troubleshooting

### Common Issues

1. **Email Not Sending**:
   - Check SendGrid API key is correct
   - Verify sender email is authenticated
   - Check console logs for error messages

2. **API Key Issues**:
   - Ensure API key has "Mail Send" permissions
   - Verify API key is not expired
   - Check SendGrid account status

3. **Email Delivery**:
   - Check spam/junk folders
   - Verify recipient email address
   - Check SendGrid activity logs

### Debug Mode

Enable detailed logging by checking console output:

```python
# Email sending status is logged
print(f"Budget overrun email sent successfully. Status: {response.status_code}")
print(f"Error sending budget overrun email: {str(e)}")
```

## API Endpoints

### Modified Endpoints

- **POST `/add_expense`**: Now includes email notification on overrun
- **POST `/check-overrun`**: Now includes email notification on overrun

### Email Function

- **`send_budget_overrun_email()`**: Internal function that sends formatted emails

## Dependencies

- **SendGrid**: `sendgrid==6.10.0` (added to requirements.txt)
- **Environment Variables**: Uses `os.environ` for configuration
- **HTML Email**: Professional email templates with CSS styling 