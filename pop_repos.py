from functions import *

failure_list = list()
failure_list.append('failure_listlist:')
path = "C:\Python36\Scripts\popular_repos\github_repo.txt"
url = read_url(path)
Output_file_name = 'output_test.txt'

#47 always failed
f=open(Output_file_name,'w+')
f.write('Name format: /user/repos,index\nNumber of branches considered is 60\nRetry times are 30\n\n')
for i in range(382,383):
	user_repos = url[i]     #/user/repos
	print ("\nname: "+user_repos,i)
	failure_list = search(user_repos,i,f,failure_list)

print (*failure_list)

#f.write(*failure_list)

f.close()	
f=open(Output_file_name,'r')
print("\nFile begins:\n")
string=f.read()
print (string)
f.close()