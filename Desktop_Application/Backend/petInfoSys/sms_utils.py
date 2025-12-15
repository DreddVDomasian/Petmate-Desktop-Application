# Desktop_Application/Backend/petInfoSys/sms_utils.py
import requests
import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)


class PhilSMSService:
    """Service for sending SMS via PhilSMS API v3"""

    def __init__(self):
        self.api_key = getattr(settings, 'PHILSMS_API_KEY', '')
        self.sender_id = getattr(settings, 'PHILSMS_SENDER_ID', 'PhilSms')
        self.api_url = getattr(settings, 'PHILSMS_API_URL', 'https://dashboard.philsms.com/api/v3/sms/send')
        self.balance_url = getattr(settings, 'PHILSMS_BALANCE_URL', 'https://dashboard.philsms.com/api/v3/sms/')

        if not self.api_key:
            raise ImproperlyConfigured("PHILSMS_API_KEY is not configured in settings")

    def send_sms(self, phone_number, message, message_type="plain"):
        """
        Send SMS via PhilSMS API

        Args:
            phone_number (str): Recipient phone number (format: 639171234567)
            message (str): SMS message content
            message_type (str): "plain" or "unicode" for special characters

        Returns:
            dict: Response from PhilSMS API
        """
        # Clean phone number according to PhilSMS format
        phone_number = self._clean_phone_number(phone_number)

        if not phone_number:
            return {
                'success': False,
                'error': 'Invalid phone number format'
            }

        # Prepare headers as per documentation
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Prepare payload
        payload = {
            'recipient': phone_number,
            'sender_id': self.sender_id,
            'type': message_type,
            'message': message
        }

        try:
            logger.info(f"Sending SMS to {phone_number}")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            logger.info(f"PhilSMS API Status: {response.status_code}")

            if response.status_code in [200, 201]:
                response_data = response.json()

                if response_data.get('status') == 'success':
                    return {
                        'success': True,
                        'status': 'success',
                        'data': response_data.get('data', ''),
                        'message': 'SMS sent successfully'
                    }
                else:
                    return {
                        'success': False,
                        'status': 'error',
                        'error': response_data.get('message', 'Unknown error from PhilSMS'),
                        'response_data': response_data
                    }
            else:
                # Try to get error details
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', f"HTTP {response.status_code}")
                except:
                    error_msg = f"HTTP {response.status_code}"

                return {
                    'success': False,
                    'error': error_msg,
                    'status_code': response.status_code
                }

        except requests.exceptions.Timeout:
            error_msg = "PhilSMS API timeout"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        except requests.exceptions.RequestException as e:
            error_msg = f"PhilSMS API request error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error sending SMS: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    def _clean_phone_number(self, phone_number):
        """
        Clean and format phone number for PhilSMS API

        PhilSMS format: 639171234567 (no +, no spaces, no dashes)

        Args:
            phone_number (str): Raw phone number

        Returns:
            str: Formatted phone number in 639XXXXXXXXX format
        """
        if not phone_number:
            return None

        # Remove all non-numeric characters
        cleaned = ''.join(filter(str.isdigit, phone_number))

        # Ensure it's in the correct format
        if cleaned.startswith('0'):
            # Convert 09171234567 to 639171234567
            cleaned = '63' + cleaned[1:]
        elif cleaned.startswith('9') and len(cleaned) == 10:
            # Convert 9171234567 to 639171234567
            cleaned = '63' + cleaned
        elif cleaned.startswith('63'):
            # Already in correct format
            pass
        elif cleaned.startswith('+63'):
            # Remove the +
            cleaned = cleaned[1:]

        # Final validation
        if cleaned.startswith('63') and len(cleaned) == 12:
            return cleaned
        else:
            logger.warning(f"Phone number format may be incorrect: {cleaned}")
            return cleaned  # Return anyway, let API handle validation

    def check_balance(self):
        """
        Check remaining SMS credits (units) and profile info via PhilSMS Profile API.

        Returns:
            dict: Contains SMS unit balance, used units, and other profile details.
        """
        try:
            # Set the correct API endpoint for balance/profile
            balance_url = "https://dashboard.philsms.com/api/v3/balance"

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            response = requests.get(
                balance_url,
                headers=headers,
                timeout=10
            )

            logger.info(f"Balance API Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    # The 'data' field contains the details about SMS units
                    balance_data = data.get('data', {})
                    return {
                        'success': True,
                        'status': 'success',
                        'message': 'Balance retrieved successfully',
                        'data': balance_data  # Contains total remaining units, used units, etc.
                    }
                else:
                    return {
                        'success': False,
                        'status': 'error',
                        'error': data.get('message', 'Unknown error from PhilSMS API')
                    }
            else:
                # Handle HTTP errors
                return {
                    'success': False,
                    'error': f"API returned HTTP {response.status_code}",
                    'status_code': response.status_code,
                    'response_text': response.text
                }

        except requests.exceptions.Timeout:
            logger.error("PhilSMS Balance API timeout")
            return {
                'success': False,
                'error': 'API timeout while checking balance'
            }
        except Exception as e:
            logger.error(f"Error checking SMS balance: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    # In sms_utils.py, add this function:


    def send_bulk_sms(self, phone_numbers, message, message_type="plain"):
        """
        Send SMS to multiple recipients

        Args:
            phone_numbers (list): List of phone numbers
            message (str): SMS message content
            message_type (str): "plain" or "unicode"

        Returns:
            dict: Bulk sending results
        """
        # Clean all phone numbers
        cleaned_numbers = []
        for number in phone_numbers:
            cleaned = self._clean_phone_number(number)
            if cleaned:
                cleaned_numbers.append(cleaned)

        if not cleaned_numbers:
            return {
                'success': False,
                'error': 'No valid phone numbers provided'
            }

        # Join with comma as per API documentation
        recipients = ','.join(cleaned_numbers)

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        payload = {
            'recipient': recipients,
            'sender_id': self.sender_id,
            'type': message_type,
            'message': message
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code in [200, 201]:
                response_data = response.json()

                if response_data.get('status') == 'success':
                    return {
                        'success': True,
                        'status': 'success',
                        'data': response_data.get('data', ''),
                        'count': len(cleaned_numbers),
                        'message': f'SMS sent to {len(cleaned_numbers)} recipients'
                    }
                else:
                    return {
                        'success': False,
                        'error': response_data.get('message', 'Unknown error')
                    }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response': response.text
                }

        except Exception as e:
            logger.error(f"Error sending bulk SMS: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

def has_sufficient_sms_balance(minimum_units=1):
    """
    Check if there are enough SMS units for sending

    Args:
        minimum_units (int): Minimum units needed (default: 1)

    Returns:
        tuple: (has_balance, balance_info, message)
    """
    sms_service = PhilSMSService()
    balance_result = sms_service.check_balance()

    if not balance_result.get('success'):
        # If can't check balance, assume insufficient (fail-safe)
        return False, None, "Could not check SMS balance"

    balance_data = balance_result.get('data', {})

    # Parse the balance - PhilSMS returns string like '₱286'
    balance_str = balance_data.get('remaining_balance', '₱0')

    try:
        # Extract numeric value from '₱286'
        balance_amount = float(balance_str.replace('₱', '').strip())

        if balance_amount >= minimum_units:
            return True, balance_data, f"SMS balance: {balance_str}"
        else:
            return False, balance_data, f"Insufficient SMS balance: {balance_str}"

    except (ValueError, AttributeError):
        # If parsing fails, check other possible formats
        if 'remaining_balance' in balance_data:
            return True, balance_data, f"SMS balance available"
        return False, balance_data, "Could not determine SMS balance"
    # Helper function specifically for appointment reminders

def send_appointment_reminder_sms(phone_number, patient_name, pet_name, service_type,
                                  appointment_date, appointment_time, booking_id, reminder_type='appointment'):
    """
    Send appointment reminder SMS

    Args:
        phone_number (str): Patient's phone number
        patient_name (str): Patient's name
        pet_name (str): Pet's name
        service_type (str): Type of service
        appointment_date (str): Appointment date
        appointment_time (str): Appointment time
        booking_id (str): Booking ID
        reminder_type (str): 'appointment' or 'service_return'

    Returns:
        dict: SMS sending result
    """
    sms_service = PhilSMSService()

    # Format the date nicely
    from datetime import datetime
    try:
        if isinstance(appointment_date, str):
            date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        else:
            formatted_date = appointment_date.strftime('%B %d, %Y')
    except:
        formatted_date = str(appointment_date)

    # Create message based on reminder type
    if reminder_type == 'appointment':
        message = (
            f"PetMate Animal Clinic Reminder: Hi {patient_name}, "
            f"your appointment for {pet_name} ({service_type}) "
            f"is on {formatted_date} at {appointment_time}. "
            f"Booking ID: {booking_id}"
        )
    elif reminder_type == 'service_return':
        message = (
            f"PetMate Animal Clinic Reminder: Hi {patient_name}, "
            f"{pet_name}'s {service_type} return visit "
            f"is scheduled for {formatted_date}. "
            f"Please visit us for follow-up care."
        )
    else:
        message = (
            f"PetMate Animal Clinic: Hi {patient_name}, "
            f"reminder for {pet_name}'s {service_type} "
            f"on {formatted_date}. Thank you!"
        )

    # Ensure message length is reasonable
    if len(message) > 160:
        # Create shorter version
        message = (
            f"PetMate Reminder: Hi {patient_name}, "
            f"{pet_name}'s {service_type} "
            f"on {formatted_date}. "
            f"ID: {booking_id}"
        )

    return sms_service.send_sms(phone_number, message)

def send_service_return_reminder_sms(phone_number, patient_name, pet_name, service_type,
                                    return_date, service_id):
        """
        Send service return reminder SMS

        Args:
            phone_number (str): Patient's phone number
            patient_name (str): Patient's name
            pet_name (str): Pet's name
            service_type (str): Type of service
            return_date (str): Return date
            service_id (str/init): Service ID

        Returns:
            dict: SMS sending result
        """
        sms_service = PhilSMSService()

        # Format date
        from datetime import datetime
        try:
            if isinstance(return_date, str):
                date_obj = datetime.strptime(return_date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%B %d, %Y')
            else:
                formatted_date = return_date.strftime('%B %d, %Y')
        except:
            formatted_date = str(return_date)

        # Create message for service return
        message = (
            f"PetMate Animal Clinic: Hi {patient_name}, "
            f"{pet_name}'s {service_type} return visit "
            f"is scheduled for {formatted_date}. "
            f"Please visit us for follow-up care."
        )

        # Ensure message length is reasonable
        if len(message) > 160:
            message = (
                f"PetMate Reminder: {patient_name}, "
                f"{pet_name}'s {service_type} return "
                f"on {formatted_date}. Service ID: {service_id}"
            )

        return sms_service.send_sms(phone_number, message)