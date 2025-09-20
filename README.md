# P2P-File-Transfer-System
A full-stack project demonstrating peer-to-peer (P2P) file transfer between two devices over a network.  
Built as part of Distributed Computer Networks (DCN), this project provides a simple yet robust interface to connect two devices and securely transfer files.

---

## Features
- **Direct P2P Connection** – Connect two devices by entering sender and receiver IP addresses.
- **Drag & Drop Interface** – Easily add files to a staging area before transfer.
- **File Management** – Cancel unwanted files before final transfer.
- **Instant File Transfer** – Supports file transfer up to **20 MB** within seconds.
- **Data Integrity** – Files remain safe, uncorrupted, and identical after transfer.
- **Secure Disconnect** – End connection with a single click after transfer.

---

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Node.js / Python (depending on your implementation)  
- **Networking:** Socket Programming (P2P Communication)  
- **Database (if any):** —  

---

## How It Works
1. Enter **Sender IP** and **Receiver IP**.  
2. Press **Connect** → Connection established.  
   - If connection fails → Error message shown.  
3. Drag & drop files into the **Sender’s staging area**.  
4. Review files:  
   - Press `x` to cancel unwanted files.  
   - Drag files to **Receiver’s area** to transfer.  
5. Files are delivered securely to the **Receiver’s shared folder**.  
6. Press **Disconnect** to safely terminate the session.
