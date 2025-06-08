# Web Teknoloji Analiz Aracı
# author: h4ck3dbyt0g1

import requests
from bs4 import BeautifulSoup
import json
import re
from fpdf import FPDF  

class WebTechAnalyzer:
    def __init__(self, url):
        self.url = self.prepare_url(url)
        self.headers = {}
        self.html = ''
        self.technologies = []
        self.signatures = self.load_signatures()
        self.licenses = []

    def prepare_url(self, url):
        if not url.startswith("http"):
            return f"http://{url}"
        return url

    def fetch(self):
        try:
            response = requests.get(self.url, timeout=10)
            self.headers = response.headers
            self.html = response.text
        except Exception as e:
            print(f"[!] Hata: {e}")

    def load_signatures(self):
        try:
            with open("web-tech-analyzer/signatures.json") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Signature dosyasi yuklenemedi: {e}")
            return {}

    def analyze_headers(self):
        server = self.headers.get("Server")
        powered = self.headers.get("X-Powered-By")
        if server:
            self.technologies.append(f"Server: {server}")
        if powered:
            self.technologies.append(f"Powered By: {powered}")
        for tech, sig in self.signatures.items():
            for header in sig.get("headers", []):
                if header in self.headers:
                    self.technologies.append(f"Detected: {tech} (via header: {header})")
        self.detect_cdn_waf()

    def analyze_html(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        metas = soup.find_all("meta")
        scripts = soup.find_all("script", src=True)
        links = soup.find_all("link", href=True)

        for meta in metas:
            name = meta.get("name", "").lower()
            content = meta.get("content", "").lower()
            if "generator" in name:
                self.technologies.append(f"Meta Generator: {content}")

        content_to_search = self.html.lower()
        for tech, sig in self.signatures.items():
            for pattern in sig.get("html_patterns", []):
                if re.search(pattern.lower(), content_to_search):
                    self.technologies.append(f"Detected: {tech} (via pattern: {pattern})")
            for keyword in sig.get("meta_generator", []):
                if keyword.lower() in content_to_search:
                    self.technologies.append(f"Detected: {tech} (via meta tag)")

        self.detect_css_frameworks(scripts, links)

    def detect_versions(self):
        matches = re.findall(r'ver[=\-]?(\d+\.\d+(\.\d+)*)', self.html, re.IGNORECASE)
        for match in matches:
            self.technologies.append(f"Possible Version: {match[0]}")

    def detect_js_libs(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        scripts = soup.find_all('script', src=True)
        for s in scripts:
            src = s['src']
            if any(lib in src for lib in ["jquery", "react", "vue", "bootstrap"]):
                self.technologies.append(f"JavaScript Library: {src}")

    def detect_licenses(self):
        license_paths = ["/license", "/license.txt", "/LICENSE", "/LICENSE.txt"]
        for path in license_paths:
            full_url = self.url.rstrip("/") + path
            try:
                r = requests.get(full_url, timeout=5)
                if r.status_code == 200 and len(r.text.strip()) > 10:
                    self.licenses.append({"path": path, "content_sample": r.text[:100]})
            except:
                continue

    def detect_css_frameworks(self, scripts, links):
        css_patterns = {
            "Bootstrap": r'bootstrap.*\.css',
            "Tailwind CSS": r'tailwind.*\.css',
            "Bulma": r'bulma.*\.css',
            "Foundation": r'foundation.*\.css'
        }
        sources = [tag.get('src', '') for tag in scripts] + [tag.get('href', '') for tag in links]
        for src in sources:
            for framework, pattern in css_patterns.items():
                if re.search(pattern, src, re.IGNORECASE):
                    self.technologies.append(f"CSS Framework: {framework} ({src})")

    def detect_cms_login_pages(self):
        login_paths = {
            "WordPress Login": "/wp-login.php",
            "Joomla Admin": "/administrator",
            "Drupal Login": "/user/login"
        }
        for name, path in login_paths.items():
            full_url = self.url.rstrip("/") + path
            try:
                r = requests.get(full_url, timeout=5)
                if r.status_code == 200 and "login" in r.text.lower():
                    self.technologies.append(f"Login Page Detected: {name}")
            except:
                continue

    def detect_cdn_waf(self):
        server_header = self.headers.get("Server", "").lower()
        powered_by = self.headers.get("X-Powered-By", "").lower()
        waf_patterns = {
            "Cloudflare": ["cloudflare"],
            "Sucuri": ["sucuri"],
            "Akamai": ["akamai", "akamaighost"],
            "Imperva / Incapsula": ["incapsula"],
            "Amazon AWS": ["amazon"],
            "Azure": ["microsoft", "azure"]
        }
        for provider, keywords in waf_patterns.items():
            for keyword in keywords:
                if keyword in server_header or keyword in powered_by:
                    self.technologies.append(f"CDN/WAF: {provider}")

    def save_as_pdf(self, data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Web Technology Report", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"URL: {data['url']}", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Technologies Detected:", ln=True)
        pdf.set_font("Arial", size=11)
        for tech in data["technologies"]:
            pdf.multi_cell(0, 10, f"- {tech}")

        if data["licenses"]:
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt="License Files:", ln=True)
            pdf.set_font("Arial", size=11)
            for lic in data["licenses"]:
                sample = lic["content_sample"].replace("\n", " ").strip()
                pdf.multi_cell(0, 10, f"- {lic['path']} (Sample: {sample}...)")

        pdf.output("report.pdf")
        print("[+] PDF raporu oluşturuldu: report.pdf")

    def run(self):
        self.fetch()
        if not self.html:
            print("[!] Sayfa cekilemedi.")
            return
        print(f"[+] Analiz ediliyor: {self.url}\n")
        self.analyze_headers()
        self.analyze_html()
        self.detect_versions()
        self.detect_js_libs()
        self.detect_licenses()
        self.detect_cms_login_pages()

        print("[+] Tespit Edilen Teknolojiler:")
        for tech in sorted(set(self.technologies)):
            print(f" - {tech}")

        if self.licenses:
            print("\n[+] Lisans Dosyalari:")
            for lic in self.licenses:
                print(f" - {lic['path']} (Sample: {lic['content_sample']}...)")

        output = {
            "url": self.url,
            "technologies": list(set(self.technologies)),
            "licenses": self.licenses
        }

        format_choice = input("\nÇıktı formatı seçin (json/pdf/her ikisi): ").strip().lower()

        if format_choice in ["json", "her ikisi", "ikisi"]:
            with open("report.json", "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            print("[+] JSON raporu oluşturuldu: report.json")

        if format_choice in ["pdf", "her ikisi", "ikisi"]:
            self.save_as_pdf(output)

if __name__ == "__main__":
    target = input("Hedef URL: ")
    analyzer = WebTechAnalyzer(target)
    analyzer.run()
