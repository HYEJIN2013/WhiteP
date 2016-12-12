#this program will delete existing index.php (if present) in html tree, and copy new index.php file from another directory ie .. to html directory.
#future plan adding feature to rename the unwanted file names without any spaces.
import shutil,os
index = "/index.php"
for folderName, subfolders, filenames in os.walk('/var/www/html'):
    print('The current folder is ' + folderName)
    
    for subfolder in subfolders:
        print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
        
    for filename in filenames:
        print('FILE INSIDE ' + folderName + ': '+ filename)
        if filename.endswith('index.php'):
        	os.unlink(filename)
        	
    shutil.copy('/var/www/index.php',folderName+index)
 
        		
    print('')
