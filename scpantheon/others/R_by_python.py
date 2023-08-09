# 'D:\R\R-4.3.1\bin\Rscript.exe'
import subprocess
R_script = 'C:/Users/23606/Documents/Workspace/Pantheon/scpantheon/others/R_test.R'
# R_script = 'C:/Users/23606/Documents/Workspace/Pantheon/scpantheon/others/r_tes.R'
retcode = subprocess.call(['D:/R/R-4.3.1/bin/Rscript.exe', '--vanilla', 
                           R_script], shell=True)