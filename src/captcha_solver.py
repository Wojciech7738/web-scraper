import requests
class CaptchaSolver:
    def __init__(self):
        API_KEY = "YOUR_2CAPTCHA_API_KEY"  # API key from 2Captcha
        site_key = "SITE_KEY_CAPTCHA"      # Site-key reCAPTCHA (can be found in the page's code)
        url = "https://example.com"        # URL of the page with CAPTCHA

        # Submit CAPTCHA for solving
        response = requests.post("http://2captcha.com/in.php", data={
            "key": API_KEY,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": url
        })

        # Retrieve the ID of the submitted CAPTCHA
        captcha_id = response.text.split('|')[1]

    # Wait for the solution
    import time
    captcha_solution = None
    while not captcha_solution:
        time.sleep(5)  # Wait 5 seconds for the response
        solution_response = requests.get(f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}")
        if solution_response.text.startswith("OK|"):
            captcha_solution = solution_response.text.split('|')[1]

    print("CAPTCHA solution:", captcha_solution)

    # Use the solution token in Selenium
    captcha_token = captcha_solution

    # Insert the token into the recaptcha field (if required by the page)
    driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{captcha_token}';")
