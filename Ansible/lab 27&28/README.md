**Lab 27** and **Lab 28**:
- **Lab 27 (Securing Sensitive Data with Ansible Vault):** Automated MySQL deployment using an Ansible Role, database creation (`ivolve`), user creation (`ivolveuser`) with full privileges, encrypting sensitive credentials with **Ansible Vault**, and validating database access on the managed node.
- **Lab 28 (Automated Host Discovery with Ansible Dynamic Inventory):** Automatically discovering and managing running AWS EC2 instances tagged with `server: ivolve` using the `amazon.aws.aws_ec2` dynamic inventory plugin, testing host connectivity, running playbooks, and verifying configuration.

---

## 📁 Project Architecture & File Tree

```text
ansible-labs-27-28/
├── ansible.cfg                # Ansible configuration file (inventory, SSH key, plugins)
├── aws_ec2.yaml               # AWS Dynamic Inventory plugin configuration
├── playbook.yml               # Main Playbook applying the MySQL role to discovered EC2 hosts
├── requirements.yml           # Required Ansible collections (amazon.aws, community.mysql)
├── my-k8s-key.pem             # EC2 Private SSH Key
├── roles/
│   └── mysql/
│       ├── tasks/
│       │   └── main.yml       # MySQL installation, DB/User creation & validation tasks
│       └── vars/
│           ├── main.yml       # Non-sensitive variables (db_name, db_user)
│           ├── vault.yml      # Encrypted secrets via Ansible Vault (vault_db_password)
│           └── vault.example.yml # Template for required vault variables
└── README.md                  # Complete documentation and execution guide
```

---

## ⚙️ Prerequisites & Setup

### 1. Control Node Requirements (Ubuntu / WSL)
Install Python, pip, Ansible, and required AWS SDK libraries:
```bash
sudo apt update && sudo apt install -y python3-pip curl unzip git software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible
pip3 install boto3 botocore
```

### 2. Install Required Ansible Collections
Install the required collections defined in `requirements.yml`:
```bash
ansible-galaxy collection install -r requirements.yml
```

### 3. Configure AWS CLI
Authenticate with your AWS account:
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region name: eu-north-1 (or your EC2 region)
# Default output format: json
```

> **Note:** Ensure your IAM user has `AmazonEC2ReadOnlyAccess` permissions or higher.

---

## 🚀 Step-by-Step Implementation

### Step 1: AWS EC2 Setup (Lab 28)
1. Launch an EC2 Instance (Ubuntu 22.04 or 24.04 LTS).
2. Attach the required tag:
   - **Key:** `server`
   - **Value:** `ivolve`
3. Configure the **Security Group**:
   - Allow Inbound Traffic on **Port 22 (SSH)** from your IP/Control Node.
4. Note your SSH Key Pair name (e.g., `my-k8s-key.pem`).

---

### Step 2: Configure SSH Key & Permissions
In Linux / WSL, SSH requires private keys to have strict permissions (`400`):
```bash
mkdir -p ~/.ssh
cp my-k8s-key.pem ~/.ssh/my-k8s-key.pem
chmod 400 ~/.ssh/my-k8s-key.pem
```

Verify permissions:
```bash
ls -l ~/.ssh/my-k8s-key.pem
# Expected output: -r-------- 1 user user ... /home/user/.ssh/my-k8s-key.pem
```

---

### Step 3: Configure Dynamic Inventory (`aws_ec2.yaml`)
The dynamic inventory is configured to automatically discover running instances matching `tag:server=ivolve`:

```yaml
plugin: amazon.aws.aws_ec2
regions:
  - eu-north-1  # Set your AWS region

filters:
  tag:server: ivolve
  instance-state-name: running

keyed_groups:
  - prefix: tag
    key: tags

compose:
  ansible_host: public_ip_address
```

---

### Step 4: Verify Dynamic Host Discovery (Lab 28 Requirement)
1. **List target hosts using `ansible-inventory`:**
   ```bash
   ansible-inventory -i aws_ec2.yaml --graph
   ```
   **Output:**
   ```text
   @all:
     |--@tag_server_ivolve:
     |  |-- ec2-xx-xx-xx-xx.eu-north-1.compute.amazonaws.com
   ```

2. **Test host connectivity via Ping:**
   ```bash
   ansible tag_server_ivolve -i aws_ec2.yaml -m ping
   ```
   **Output:**
   ```json
   ec2-xx-xx-xx-xx.eu-north-1.compute.amazonaws.com | SUCCESS => {
       "ansible_facts": {
           "discovered_interpreter_python": "/usr/bin/python3"
       },
       "changed": false,
       "ping": "pong"
   }
   ```

---

### Step 5: Secure Sensitive Data with Ansible Vault (Lab 27 Requirement)
Create the encrypted secrets file:
```bash
ansible-vault create roles/mysql/vars/vault.yml
```
You will be prompted to set a vault password. Add the following variables:
```yaml
---
vault_db_password: "YourSecurePassword2026!"
vault_mysql_root_password: "YourRootPassword2026!"
```

To edit the encrypted file in the future:
```bash
ansible-vault edit roles/mysql/vars/vault.yml
```

---

### Step 6: Deploy the Playbook
Execute the playbook against the dynamically discovered EC2 host:

```bash
export ANSIBLE_CONFIG=./ansible.cfg
ansible-playbook -i aws_ec2.yaml playbook.yml --ask-vault-pass
```

Enter your Vault password when prompted.

#### What this Playbook automates:
1. Gathers facts from the dynamically discovered EC2 node (`tag_server_ivolve`).
2. Installs `mysql-server` and `python3-pymysql`.
3. Starts and enables the MySQL systemd service.
4. Creates the database `ivolve`.
5. Creates the database user `ivolveuser` with full privileges on `ivolve.*`.
6. Executes the validation task: connects to MySQL as `ivolveuser`, executes `SHOW DATABASES;`, and asserts that `ivolve` is present and accessible.

---

## 🔍 Validation & Verification (Lab 27 & 28)

### 1. Automated Validation (Inside the Playbook)
The playbook executes an assertion check on the target node:
```yaml
- name: Validate database connection by connecting as 'ivolveuser' and listing databases
  ansible.builtin.command: >
    mysql -u {{ db_user }} -p'{{ vault_db_password }}' -e "SHOW DATABASES;"
  register: mysql_validation_output
  changed_when: false

- name: Assert that 'ivolve' database is present
  ansible.builtin.assert:
    that:
      - "db_name in mysql_validation_output.stdout"
    success_msg: "Validation Succeeded: Database 'ivolve' is present and accessible by 'ivolveuser'!"
```

### 2. Manual Verification on the Managed Node
SSH into the EC2 instance:
```bash
ssh -i ~/.ssh/my-k8s-key.pem ubuntu@<EC2_PUBLIC_IP>
```

Connect to the database using the newly created user `ivolveuser`:
```bash
mysql -u ivolveuser -p
```
*(Enter the password configured in `vault_db_password`)*

Run the SQL queries:
```sql
SHOW DATABASES;
```

**Expected Output:**
```text
+--------------------+
| Database           |
+--------------------+
| information_schema |
| ivolve             |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)
```

Verify privileges on the `ivolve` database:
```sql
USE ivolve;
CREATE TABLE connection_test (id INT, message VARCHAR(100));
INSERT INTO connection_test VALUES (1, 'Lab 27 & 28 Verified');
SELECT * FROM connection_test;
EXIT;
```

---

## 🛠️ Troubleshooting & Best Practices

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `WARNING: Ansible is being run in a world writable directory` | Running inside Windows mount (`/mnt/c/`) in WSL | Run `export ANSIBLE_CONFIG=./ansible.cfg` or explicitly pass `-i aws_ec2.yaml`. |
| `Permissions 0555 are too open` | Storing `.pem` key on NTFS Windows partition | Copy key to native Linux path: `cp key.pem ~/.ssh/` and run `chmod 400 ~/.ssh/key.pem`. |
| `Could not match supplied host pattern: tag_server_ivolve` | Region mismatch or EC2 not tagged/running | Verify region in `aws_ec2.yaml` matches the EC2 region (`eu-north-1`), and ensure EC2 tag is `server=ivolve`. |
| `Access denied for user 'ivolveuser'@'localhost'` | Using Vault decryption password instead of DB password | Enter the password defined in `vault_db_password` inside `vault.yml`, not the vault unlock password. |
