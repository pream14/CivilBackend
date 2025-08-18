#!/usr/bin/env python3
"""
Test script for the automatic report generation feature.
This script tests the PDF and Excel report generation endpoints.
"""

import requests
import json
import os
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
TEST_PROJECT = "Highway Masterplan"  # Replace with an existing project name
TEST_USER_ID = "USER001"  # Replace with an existing user ID

def test_project_report_pdf():
    """Test project report PDF generation"""
    print("Testing Project Report PDF Generation...")
    
    url = f"{BASE_URL}/download-project-report-pdf"
    params = {
        'projectname': TEST_PROJECT,
        'type': 'employee'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Save the PDF file
            filename = f"test_project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ PDF report generated successfully: {filename}")
            return True
        else:
            print(f"❌ Failed to generate PDF report. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing PDF generation: {str(e)}")
        return False

def test_project_report_excel():
    """Test project report Excel generation"""
    print("Testing Project Report Excel Generation...")
    
    url = f"{BASE_URL}/download-project-report-excel"
    params = {
        'projectname': TEST_PROJECT,
        'type': 'category'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Save the Excel file
            filename = f"test_project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Excel report generated successfully: {filename}")
            return True
        else:
            print(f"❌ Failed to generate Excel report. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Excel generation: {str(e)}")
        return False

def test_user_financial_report_pdf():
    """Test user financial report PDF generation"""
    print("Testing User Financial Report PDF Generation...")
    
    url = f"{BASE_URL}/download-user-financial-report-pdf"
    params = {
        'id': TEST_USER_ID,
        'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'end_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Save the PDF file
            filename = f"test_user_financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ User financial PDF report generated successfully: {filename}")
            return True
        else:
            print(f"❌ Failed to generate user financial PDF report. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing user financial PDF generation: {str(e)}")
        return False

def test_user_financial_report_excel():
    """Test user financial report Excel generation"""
    print("Testing User Financial Report Excel Generation...")
    
    url = f"{BASE_URL}/download-user-financial-report-excel"
    params = {
        'id': TEST_USER_ID,
        'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'end_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            # Save the Excel file
            filename = f"test_user_financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ User financial Excel report generated successfully: {filename}")
            return True
        else:
            print(f"❌ Failed to generate user financial Excel report. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing user financial Excel generation: {str(e)}")
        return False

def test_error_handling():
    """Test error handling for invalid requests"""
    print("Testing Error Handling...")
    
    # Test missing project name
    url = f"{BASE_URL}/download-project-report-pdf"
    params = {'type': 'employee'}  # Missing projectname
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 400:
            print("✅ Error handling works correctly for missing project name")
            return True
        else:
            print(f"❌ Expected 400 error, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing error handling: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Report Generation Tests")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/projects")
        if response.status_code != 200:
            print("❌ Server is not running or not accessible")
            print("Please start the Flask application first: python app.py")
            return
    except Exception as e:
        print("❌ Cannot connect to server")
        print("Please start the Flask application first: python app.py")
        return
    
    print("✅ Server is running and accessible")
    print()
    
    # Run tests
    tests = [
        test_project_report_pdf,
        test_project_report_excel,
        test_user_financial_report_pdf,
        test_user_financial_report_excel,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
        print()
    
    # Summary
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Report generation feature is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
    
    print("\n📁 Generated test files are saved in the current directory.")
    print("You can open them to verify the report format and content.")

if __name__ == "__main__":
    main() 