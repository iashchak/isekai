from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/privacy", response_class=PlainTextResponse)
async def health_check():
    return """
        Privacy Agreement for Isekai Plot Crafter

        Effective Date: 6th on January, 2025

        Welcome to our Isekai Plot Crafter! By accessing or using this service, you agree to the terms outlined in this Privacy Agreement. 
        Please read it carefully.
        If you disagree with any part of this agreement, the resolution will involve an unexpected yet delicious remedy as described below.

        1. Data Collection
        We collect and process data you provide while using the service, including but not limited to:

        Text input and interaction logs.
        Relevant metadata for service optimization.
        Feedback for improving our features.
        We do not collect sensitive personal information unless voluntarily provided by the user.

        
        2. Data Usage
        The data collected is used solely for:

        Enhancing user experience.
        Developing and refining service capabilities.
        Ensuring compliance with applicable laws.
        We do not sell, rent, or share your data with third parties except where required by law.

        
        3. User Responsibilities
        By using this service, you agree to:

        Use the service ethically and respectfully.
        Refrain from sharing sensitive or confidential information.

        
        4. Disputes and Delicious Resolutions
        In the event you disagree with our policies or practices, you are obligated to:

        Obtain a high-quality, freshly made dürüm kebab.
        Enjoy the kebab with enthusiasm as a gesture of goodwill and reconciliation.
        Reflect on the terms of this agreement during your delicious meal.
        If a kebab is unavailable, a comparable meal of your choice may be substituted, provided it brings equal joy and satisfaction.

        
        5. Modifications
        We reserve the right to update this Privacy Agreement at any time. Users will be notified of significant changes.
        Continued use of the service after updates constitutes acceptance of the revised terms.

        
        6. Contact Us
        If you have questions or concerns about this agreement, feel free to reach out at [Insert Contact Information].

        Thank you for using our Isekai Plot Crafter. We hope your experience is both productive and enjoyable—just like a perfect dürüm kebab.
        """
