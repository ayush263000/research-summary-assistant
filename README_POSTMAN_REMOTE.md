# 🌐 Using Document GenAI Assistant from Another PC

## 📋 **Setup Instructions for Remote Users**

### **Prerequisites**
1. Postman installed on your computer
2. Network access to the host PC
3. The collection and environment files

### **Files Needed**
- `postman_collection.json` - API endpoints collection
- `postman_environment.json` - Environment variables

## 🔧 **Import Setup**

### **Step 1: Import Collection**
1. Open Postman
2. Click **Import** (top left)
3. Drag and drop `postman_collection.json`
4. Click **Import**

### **Step 2: Import Environment**
1. Click **Import** again
2. Drag and drop `postman_environment.json`
3. Click **Import**

### **Step 3: Configure Network Access**
1. Select **"Document GenAI Assistant Environment"** from the dropdown (top right)
2. Click the **eye icon** next to the environment dropdown
3. Click **Edit** on the environment

### **Step 4: Update Base URL**
Find your host's IP address and update these variables:

#### **Option A: Use Local Network IP**
```
base_url: http://192.168.1.XXX:8000
```
Replace `192.168.1.XXX` with the actual IP address of the host PC.

#### **Option B: Use Public IP (if exposed)**
```
base_url: http://PUBLIC_IP:8000
```

#### **Option C: Use ngrok or similar tunnel**
```
base_url: https://your-tunnel-url.ngrok.io
```

## 🔍 **Finding the Host IP Address**

### **Host PC needs to share their IP:**

#### **On macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

#### **On Windows:**
```cmd
ipconfig | findstr "IPv4"
```

#### **On Linux:**
```bash
hostname -I
```

## 📱 **Testing Connection**

### **Step 1: Test Health Check**
1. Select the environment with updated IP
2. Go to **🏥 Health & Status** folder
3. Click **Health Check**
4. Click **Send**
5. Should return: `{"status": "healthy", "version": "1.0.0"}`

### **Step 2: Test Document Upload**
1. Go to **📄 Document Management** folder
2. Click **Upload Document**
3. In **Body** tab, select a test file
4. Click **Send**
5. Should return document_id and summary

### **Step 3: Test Q&A**
1. Go to **❓ Question & Answer** folder
2. Click **Ask Question**
3. The `document_id` should auto-populate from previous upload
4. Click **Send**

## 🛠️ **Troubleshooting**

### **Connection Refused Error**
- ✅ Verify the host PC is running the server
- ✅ Check if the IP address is correct
- ✅ Ensure firewall allows connections on ports 8000/8501
- ✅ Confirm you're on the same network (or have proper routing)

### **404 Not Found**
- ✅ Verify the server is running on the correct port
- ✅ Check the base_url format (include http://)

### **Timeout Errors**
- ✅ Check network connectivity: `ping HOST_IP`
- ✅ Verify firewall settings on host PC
- ✅ Try different network (mobile hotspot test)

### **File Upload Issues**
- ✅ File must be PDF or TXT format
- ✅ File size must be under 50MB
- ✅ Select file in the "file" field, not text

## 🔧 **Environment Variables Reference**

| Variable | Purpose | Example |
|----------|---------|---------|
| `base_url` | API server URL | `http://192.168.1.100:8000` |
| `base_url_network` | Network accessible URL | `http://192.168.1.100:8000` |
| `streamlit_url` | Frontend URL | `http://192.168.1.100:8501` |
| `document_id` | Auto-populated after upload | `doc_abc123xyz` |

## 🌍 **Network Types**

### **Same WiFi Network (Easiest)**
- Use local IP address (192.168.x.x or 10.x.x.x)
- Host PC allows connections on port 8000

### **Different Networks**
- Requires port forwarding or VPN
- Use public IP or tunnel service
- May need router configuration

### **Using Tunnel Services (Recommended for Testing)**

#### **ngrok (Free)**
Host PC runs:
```bash
# Install ngrok
npm install -g ngrok

# Expose port 8000
ngrok http 8000
```

Then use the ngrok URL in Postman:
```
base_url: https://abc123.ngrok.io
```

#### **localtunnel (Free)**
Host PC runs:
```bash
# Install localtunnel
npm install -g localtunnel

# Expose port 8000
lt --port 8000
```

## 📞 **Support Checklist**

Before asking for help, verify:
- [ ] Postman collection imported successfully
- [ ] Environment selected and configured
- [ ] Host PC server is running (`python run.py`)
- [ ] IP address is correct and accessible
- [ ] Firewall allows connections
- [ ] Health check returns 200 OK

## 🎯 **Quick Test Sequence**
1. Health Check → Should return 200 OK
2. Upload Document → Should return document_id
3. Ask Question → Should return AI answer
4. Generate Challenge → Should return questions
5. Evaluate Answer → Should return score

Happy Testing! 🚀
