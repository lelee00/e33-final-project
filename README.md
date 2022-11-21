# i535-final-project
Data and Code for I535 Final Project

Instructions to use this code:

1. Create a new project in Google Cloud Platform. 
2. Create a new Compute Engine VM instance: 
   
   * Navigation Menu (top left) $\rightarrow$ Compute Engine $\rightarrow$ VM Instances $\rightarrow$ Create Instance  
   * ### Instance settings  
      * **Name:** *Your Choice*  
      * **Region:** *Default*
      * **Zone:** *Default*  
      * **Boot Disk:** *Change*   
      * **Version:** *Debian GNU/Linux 10 (buster)*
      * **Create**
 3. When running, SSH into your newly created VM instance (select '**SSH**' next to the VM name)
 4. Run the following commands in the SSH shell:

      `sudo apt-get update`
      
      `sudo apt-get -y -qq install git`
      
      `git clone https://github.com/lelee00/i535-final-project.git`
      
      `cd i535-final-project/`
      
5. Going back to the Google Cloud Platform console, create a new Cloud Storage Bucket:

   * Navigation Menu (top left) $\rightarrow$ Cloud Storage $\rightarrow$ Buckets $\rightarrow$ Create 
   * ### Bucket Settings
      * **Name:** *Your Choice, MAKE NOTE OF BUCKET NAME*
      * **Storage:** *Leave as Multi-Regional OR reduce costs by selecting regional $\rightarrow$ [same region as your VM instance]*
      * **Choose How to Control Access to Objects:**    
         * **Prevent Public Access:** *Uncheck 'Enforce public access prevention'* 
         * **Access Control:** *Fine-Grained*
      * **Create**
6. Return to the cloud shell
7. Run the following command:
   
   `python3 transform_visualize.py [YOUR BUCKET NAME HERE]`
8. Publish visualization
   
   * Navigate to Cloud Storage Bucket $\rightarrow$ /nutrition/
   * Click the three dots at the end of the `us-obesity.html` file
   * Click **Edit Access**
   * Click **Add Entry**
   * Select
      * **Entity:** *Public*
      * **Name:** *allUsers*
      * **Access:** *Reader*
      * **Save**
      
The visualization should now be published to `https://storage.googleapis.com/[YOUR BUCKET NAME HERE]/nutrition/us-obesity.html` !

      
