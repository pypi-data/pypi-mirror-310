"""
Company Name: Parendum OÜ
Creation Date: September 2023
Copyright © 2024 Parendum OÜ. All rights reserved.

Description:
This file is part of Parendum Astra Api library.
Unauthorized use, reproduction, modification, or distribution without the
express consent of Parendum OÜ is strictly prohibited.

Contact:
info@parendum.com
https://parendum.com
"""

from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from base64 import b64decode
import requests
import hashlib
import json
import hmac
import time


class ParendumAstraAPI:
    """
    A client for interacting with the Parendum Astra API.

    Attributes:
        api_key (str): The API key for authentication.
        api_secret (str): The API secret for generating signatures.
        endpoint (str): The base URL for the API.
    """

    def __init__(self, api_key: str, api_secret: str, endpoint: str = "https://astraportal.parendum.com"):
        """
        Initialize the ParendumAstraAPI client.

        Args:
            api_key (str): The API key for authentication.
            api_secret (str): The API secret for generating signatures.
            endpoint (str): The API endpoint to communicate with.
        """
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.endpoint = endpoint

    def _generate_signature(self, timestamp: str) -> str:
        """
        Generate HMAC signature using the provided timestamp.

        Args:
            timestamp (str): The timestamp to be used in signature generation.

        Returns:
            str: The generated HMAC signature.
        """
        return hmac.new(self.api_secret, timestamp.encode(), digestmod=hashlib.sha256).hexdigest()

    def _get_hmac_headers(self) -> dict:
        """
        Generate the HMAC headers required for API requests.

        Returns:
            dict: A dictionary containing the required headers.
        """
        timestamp = str(int(time.time()))
        return {
            "X-Signature": self._generate_signature(timestamp),
            "X-Timestamp": timestamp,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _decrypt_result(self, result: dict) -> dict:
        """
        Decrypt the encrypted response from the API.

        Args:
            result (dict): The encrypted API response.

        Returns:
            dict: The decrypted API response.
        """
        iv = b64decode(result.get("iv"))
        ciphertext = b64decode(result.get("ciphertext"))
        content_type = b64decode(result.get("content_type")).decode('utf-8')
        cipher = AES.new(SHA256.new(self.api_secret).digest(), AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        if content_type == "json":
            return json.loads(decrypted.decode('utf-8'))
        return b64decode(decrypted)

    def _do_post(self, url: str, body: dict = None) -> dict:
        """
        Make a POST request to the specified URL.

        Args:
            url (str): The URL to make the request to.
            body (dict, optional): The body of the request. Defaults to None.

        Returns:
            dict: The API response.
        """
        try:
            response = requests.request("POST", url, headers=self._get_hmac_headers(), json=body)
            if response.status_code == 200:
                return self._decrypt_result(response.json())
            return dict(code=response.status_code, error=response.json())
        except Exception as e:
            return dict(code=500, error=str(e))

    def get_companies(self):
        """
        Retrieve a list of companies from the API.

        Returns:
            dict: The API response containing the list of companies.
        """
        return self._do_post(self.endpoint + "/api/companies")

    def get_users(self, company: str = None):
        """
        Retrieve the users for a company from the API.

        Args:
            company (str, optional): The company code for which users are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the list of users.
        """
        return self._do_post(self.endpoint + "/api/users", dict(company=company))

    def get_assets(self, company: str = None):
        """
        Retrieve the assets for a company from the API.

        Args:
            company (str, optional): The company code for which assets are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the list of assets.
        """
        return self._do_post(self.endpoint + "/api/assets", dict(company=company))

    def get_asset_groups(self, company: str = None):
        """
        Retrieve the asset groups for a company from the API.

        Args:
            company (str, optional): The company code for which asset groups are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the list of asset groups.
        """
        return self._do_post(self.endpoint + "/api/asset_groups", dict(company=company))

    def get_scans_vm(self, company: str = None):
        """
        Retrieve the VM scans for a company from the API.

        Args:
            company (str, optional): The company code for which scans are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the list of vm scans.
        """
        return self._do_post(self.endpoint + "/api/scans/vm", dict(company=company))

    def get_scans_was(self, company: str = None):
        """
        Retrieve the WAS scans for a company from the API.

        Args:
            company (str, optional): The company code for which scans are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the list of was scans.
        """
        return self._do_post(self.endpoint + "/api/scans/was", dict(company=company))

    def get_reports(self, company: str = None):
        """
        Retrieve reports from the API.

        Args:
            company (str, optional): The company code for which reports are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the reports.
        """
        return self._do_post(self.endpoint + "/api/reports", dict(company=company))

    def get_report(self, report: str):
        """
        Retrieve a report from the API.

        Args:
            report (str): The report code.

        Returns:
            dict: The API response containing the report.
        """
        return self._do_post(self.endpoint + "/api/reports/report", dict(report=report))

    def get_report_evidences(self, report: str, vuln: str):
        """
        Retrieve the evidence images from a report from the API.

        Args:
            report (str): The report code.
            vuln (str): A vulnerability code.

        Returns:
            file: The API response contains the image file (zip file if there is more than one).
        """
        return self._do_post(self.endpoint + "/api/reports/report/evidences", dict(report=report, vuln=vuln))

    def get_phishings(self, company: str = None):
        """
        Retrieve phishing campaigns from the API.

        Args:
            company (str, optional): The company code for which phishing campaigns are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the phishing campaigns.
        """
        return self._do_post(self.endpoint + "/api/phishings", dict(company=company))

    def get_phishing_campaign(self, campaign: str):
        """
        Retrieve a phishing campaign from the API.

        Returns:
            dict: The API response containing the phishing campaign information.
        """
        return self._do_post(self.endpoint + "/api/phishings/campaign", dict(campaign=campaign))

    def get_agents(self, company: str = None):
        """
        Retrieve agents from the API.

        Args:
            company (str, optional): The company code for which agents are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the agents.
        """
        return self._do_post(self.endpoint + "/api/agents", dict(company=company))

    def get_agent(self, agent: str):
        """
        Retrieve an agent from the API.

        Returns:
            dict: The API response containing the agent information.
        """
        return self._do_post(self.endpoint + "/api/agents/agent", dict(agent=agent))

    def get_credentials(self, company: str = None):
        """
        Retrieve credentials from the API.

        Args:
            company (str, optional): The company code for which credentials are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the credentials file.
        """
        return self._do_post(self.endpoint + "/api/credentials", dict(company=company))

    def get_osint_leaks(self, company: str = None):
        """
        Retrieve OSINT leaks from the API.

        Args:
            company (str, optional): The company code for which osint leaks are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the osint leaks findings.
        """
        return self._do_post(self.endpoint + "/api/osint", dict(company=company))

    def get_osint_leak(self, leak: str):
        """
        Retrieve OSINT leak from the API.

        Args:
            leak (str): The OSINT leak code for which information is to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the osint leak information.
        """
        return self._do_post(self.endpoint + "/api/osint/leak", dict(leak=leak))

    def get_sast_projects(self, company: str = None):
        """
        Retrieve SAST projects from the API.

        Args:
            company (str, optional): The company code for which sast projects are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the sast projects.
        """
        return self._do_post(self.endpoint + "/api/sast", dict(company=company))

    def get_sast_project_findings(self, finding: str):
        """
        Retrieve findings for a SAST project from the API.

        Args:
            finding (str): The SAST project code for which findings are to be retrieved. Defaults to None.

        Returns:
            dict: The API response containing the sast project findings.
        """
        return self._do_post(self.endpoint + "/api/sast/findings", dict(finding=finding))
