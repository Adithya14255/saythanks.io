# test_runner.py
import subprocess
import time
import sys
import os
from datetime import datetime
import json
import requests

class MobileTestRunner:
    def __init__(self):
        self.start_time = datetime.now()
        self.results = {
            "start_time": self.start_time.isoformat(),
            "test_suites": {},
            "summary": {}
        }
        
    def log(self, message, color="white"):
        colors = {
            "green": "\033[92m",
            "yellow": "\033[93m", 
            "red": "\033[91m",
            "cyan": "\033[96m",
            "white": "\033[0m"
        }
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("{}[{}] {}{}".format(colors.get(color, colors['white']), timestamp, message, colors['white']))
        sys.stdout.flush()
        
    def wait_for_services(self):
        """Wait for all services to be ready"""
        # Selenium is required
        self.log("Checking Selenium...", "yellow")
        if not self.wait_for_selenium():
            self.log("❌ Selenium not ready", "red")
            return False
        self.log("✅ Selenium ready", "green")
        
        # Appium services are optional for web testing
        android_ready = False
        ios_ready = False
        
        self.log("Checking Android Appium...", "yellow")
        if self.wait_for_android():
            self.log("✅ Android Appium ready", "green")
            android_ready = True
        else:
            self.log("⚠️ Android Appium not available (skipping native app tests)", "yellow")
        
        self.log("Checking iOS Appium...", "yellow")
        if self.wait_for_ios():
            self.log("✅ iOS Appium ready", "green")
            ios_ready = True
        else:
            self.log("⚠️ iOS Appium not available (skipping native app tests)", "yellow")
        
        # Store availability for later use
        self.android_available = android_ready
        self.ios_available = ios_ready
        
        # Always return True if Selenium is ready (web testing can proceed)
        return True
        
    def wait_for_selenium(self, max_attempts=30):
        """Wait for Selenium Grid to be ready"""
        selenium_host = os.getenv('SELENIUM_HUB_HOST', 'selenium')
        selenium_port = os.getenv('SELENIUM_HUB_PORT', '4444')
        selenium_url = "http://{}:{}/wd/hub/status".format(selenium_host, selenium_port)
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(selenium_url, timeout=5)
                if response.status_code == 200:
                    status = response.json()
                    if status.get('value', {}).get('ready', False):
                        return True
            except Exception:
                pass
            time.sleep(2)
        return False
        
    def wait_for_android(self, max_attempts=30):
        """Wait for Android Appium to be ready"""
        android_host = os.getenv('ANDROID_HOST', 'android')
        android_port = os.getenv('ANDROID_PORT', '4723')
        android_url = "http://{}:{}/status".format(android_host, android_port)  # Changed from /wd/hub/status
    
        for attempt in range(max_attempts):
            try:
                response = requests.get(android_url, timeout=5)
                if response.status_code == 200:
                    return True
            except Exception:
                pass
            time.sleep(2)
        return False
    
    def wait_for_ios(self, max_attempts=30):
        """Wait for iOS Appium to be ready"""
        ios_host = os.getenv('IOS_HOST', 'ios')
        ios_port = os.getenv('IOS_PORT', '4725')
        ios_url = "http://{}:{}/status".format(ios_host, ios_port)  # Changed from /wd/hub/status
    
        for attempt in range(max_attempts):
            try:
                response = requests.get(ios_url, timeout=5)
                if response.status_code == 200:
                    return True
            except Exception:
                pass
            time.sleep(2)
        return False
        
    def run_test_suite(self, test_path, description):
        """Run a specific test suite and capture results"""
        self.log("Running {}...".format(description), "cyan")
        
        if not os.path.exists(test_path):
            self.log("⚠️ Test file not found: {}".format(test_path), "yellow")
            self.results["test_suites"][description] = {
                "success": False,
                "duration": 0,
                "return_code": -1,
                "error": "Test file not found"
            }
            return
        
        start_time = time.time()
        
        # Build pytest command with HTML reports
        html_report_name = description.lower().replace(' ', '_').replace('-', '_')
        cmd = [
            "pytest", 
            test_path,
            "-v",
            "--tb=short",
            "--html=reports/{}_report.html".format(html_report_name),
            "--self-contained-html",
            "--junit-xml=reports/{}_junit.xml".format(html_report_name)
        ]
        
        try:
            # Python 3.6 compatible subprocess call
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=300  # 5 minute timeout per test suite
            )
            
            duration = time.time() - start_time
            
            # Parse results
            success = result.returncode == 0
            
            self.results["test_suites"][description] = {
                "success": success,
                "duration": round(duration, 2),
                "return_code": result.returncode,
                "stdout": result.stdout[-1000:] if result.stdout else "",
                "stderr": result.stderr[-1000:] if result.stderr else ""
            }
            
            if success:
                self.log("✅ {} completed successfully ({:.1f}s)".format(description, duration), "green")
            else:
                self.log("❌ {} failed ({:.1f}s)".format(description, duration), "red")
                self.log("Error output: {}".format(result.stderr), "red")
                
        except subprocess.TimeoutExpired:
            self.log("⏰ {} timed out".format(description), "red")
            self.results["test_suites"][description] = {
                "success": False,
                "duration": 300,
                "return_code": -1,
                "error": "Test suite timed out"
            }
            
        except Exception as e:
            self.log("💥 {} crashed: {}".format(description, e), "red")
            self.results["test_suites"][description] = {
                "success": False,
                "duration": 0,
                "return_code": -1,
                "error": str(e)
            }
    
    def generate_summary_report(self):
        """Generate summary reports"""
        self.log("Generating summary report...", "yellow")
        
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        # Calculate summary stats
        total_suites = len(self.results["test_suites"])
        passed_suites = sum(1 for suite in self.results["test_suites"].values() if suite["success"])
        failed_suites = total_suites - passed_suites
        
        self.results["summary"] = {
            "end_time": end_time.isoformat(),
            "total_duration": round(total_duration, 2),
            "total_suites": total_suites,
            "passed_suites": passed_suites,
            "failed_suites": failed_suites,
            "success_rate": round((passed_suites / total_suites) * 100, 1) if total_suites > 0 else 0
        }
        
        # Save JSON report
        with open("reports/test_summary.json", "w") as f:
            json.dump(self.results, f, indent=2)
            
        # Generate HTML summary
        self.generate_html_summary()
        
        # Print summary to console
        self.print_summary()
        
    def generate_html_summary(self):
        """Generate HTML summary report"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>SayThanks.io Mobile Test Summary</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ background: white; border: 1px solid #ddd; border-radius: 5px; padding: 15px; flex: 1; }}
        .success {{ border-left: 4px solid #28a745; }}
        .warning {{ border-left: 4px solid #ffc107; }}
        .danger {{ border-left: 4px solid #dc3545; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .status-pass {{ color: #28a745; font-weight: bold; }}
        .status-fail {{ color: #dc3545; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 SayThanks.io Mobile Test Results</h1>
        <p>Generated: {timestamp}</p>
    </div>
    
    <div class="summary">
        <div class="card success">
            <h3>✅ Passed</h3>
            <h2>{passed}</h2>
        </div>
        <div class="card danger">
            <h3>❌ Failed</h3>
            <h2>{failed}</h2>
        </div>
        <div class="card warning">
            <h3>📊 Success Rate</h3>
            <h2>{success_rate}%</h2>
        </div>
        <div class="card">
            <h3>⏱️ Duration</h3>
            <h2>{duration}s</h2>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Test Suite</th>
                <th>Status</th>
                <th>Duration</th>
                <th>Report</th>
            </tr>
        </thead>
        <tbody>
            {test_rows}
        </tbody>
    </table>
</body>
</html>
        """.strip()
        
        # Generate test rows
        test_rows = ""
        for suite_name, suite_data in self.results["test_suites"].items():
            status_class = "status-pass" if suite_data["success"] else "status-fail"
            status_text = "✅ PASS" if suite_data["success"] else "❌ FAIL"
            html_report_name = suite_name.lower().replace(' ', '_').replace('-', '_')
            
            test_rows += """
            <tr>
                <td>{}</td>
                <td class="{}">{}</td>
                <td>{}s</td>
                <td><a href="{}_report.html">View Report</a></td>
            </tr>
            """.format(suite_name, status_class, status_text, suite_data["duration"], html_report_name)
        
        # Format the HTML
        formatted_html = html_content.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            passed=self.results["summary"]["passed_suites"],
            failed=self.results["summary"]["failed_suites"],
            success_rate=self.results["summary"]["success_rate"],
            duration=self.results["summary"]["total_duration"],
            test_rows=test_rows
        )
        
        # Save HTML report
        with open("reports/summary_report.html", "w") as f:
            f.write(formatted_html)
        
    def print_summary(self):
        """Print summary to console"""
        print("\n" + "="*60)
        self.log("📊 TEST EXECUTION SUMMARY", "cyan")
        print("="*60)
        
        summary = self.results["summary"]
        self.log("Total Duration: {}s".format(summary['total_duration']), "white")
        self.log("Total Test Suites: {}".format(summary['total_suites']), "white")
        self.log("Passed: {}".format(summary['passed_suites']), "green")
        self.log("Failed: {}".format(summary['failed_suites']), "red")
        self.log("Success Rate: {}%".format(summary['success_rate']), "green" if summary['success_rate'] > 80 else "yellow")
        
        print("\n" + "-"*60)
        self.log("📋 DETAILED RESULTS", "cyan")
        print("-"*60)
        
        for suite_name, suite_data in self.results["test_suites"].items():
            status = "✅ PASSED" if suite_data["success"] else "❌ FAILED"
            color = "green" if suite_data["success"] else "red"
            self.log("{} | {} ({:.2f}s)".format(status, suite_name, suite_data['duration']), color)
            
        print("="*60 + "\n")
        
        if self.results["summary"]["failed_suites"] == 0:
            self.log("🎉 All tests completed successfully!", "green")
        else:
            self.log("💥 Some tests failed. Check reports for details.", "red")
        
    def run_all_tests(self):
        """Run complete test suite"""
        self.log("🚀 Starting SayThanks.io Mobile Testing Suite...", "green")
        
        # Create reports directory
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        # Wait for services
        self.log("Waiting for services to be ready...", "yellow")
        if not self.wait_for_services():
            self.log("💥 Failed to connect to required services. Exiting.", "red")
            sys.exit(1)
        
        # Additional wait for stability
        time.sleep(5)
        
        # Define all test suites to run
        test_suites = [
            ("tests/mobile/cross_platform/responsive_tests.py", "Responsive Layout Tests"),
            ("tests/mobile/cross_platform/touch_tests.py", "Touch Interaction Tests"),
            ("tests/mobile/cross_platform/content_tests.py", "Content Adaptation Tests"),
            ("tests/mobile/cross_platform/javascript_tests.py", "JavaScript Functionality Tests"),
            ("tests/mobile/cross_platform/performance_tests.py", "Performance Tests"),
            ("tests/mobile/cross_platform/browser_tests.py", "Cross-Browser Tests")
        ]
        
        # Run each test suite
        for test_path, description in test_suites:
            self.run_test_suite(test_path, description)
        
        # Generate reports
        self.generate_summary_report()
        
        # Final status
        if self.results["summary"]["failed_suites"] == 0:
            self.log("🎉 All tests passed!", "green")
            sys.exit(0)
        else:
            self.log("💥 {} test suite(s) failed. Check output for details.".format(self.results['summary']['failed_suites']), "red")
            sys.exit(1)

if __name__ == "__main__":
    runner = MobileTestRunner()
    runner.run_all_tests()