import requests
import re

retry_times = 30
limit = retry_times
token =
#write file
def write_file(f,user_repos,index,star,forks,watch,license,contributors,commits,commit_total,LastDate):
	try:
		commit_total = str(commit_total)
		LastDate = str(LastDate)
		
		f.write('Name: '+user_repos+','+index+'\n')
		f.write('Star: '+star+'\n')
		f.write('Fork: '+forks+'\n')
		f.write('Watch: '+watch+'\n')
		f.write('License: '+license+'\n')
		f.write('Contributors: '+contributors+'\n')
		f.write('Commits: '+commits+'\n')
		f.write('Commits last year: '+commit_total+'\n')
		f.write('Laste commit date: '+LastDate+'\n\n\n')
	
	except: 
		print ('Write file failed')


def search(user_repos,index,f,failure_list):
	index = str(index)
	result = requests.get('https://api.github.com/repos'+user_repos+'?access_token='+token)
	s = result.text
	s = str(s)

	#search star
	try:
		temp = re.search(r'"stargazers_count":\d+,',s)
		temp1 = temp.group()
		#print (temp1)
		star = re.search(r'\d+',temp1)
		result = star
	
		if result:
			print ("Star number: "+result.group())
			star = result.group()
		else:
			print ("Star not found")
	except:
		print ("Star search failed")
		star = 'none'
	
	#search forks
	try:
		temp = re.search(r'"forks_count":\d+,',s)
		temp1 = temp.group()
		forks = re.search(r'\d+',temp1)
		result = forks
		if result:
			print ("Forks number: "+result.group())
			forks = result.group()
		else:
			print ("Fork not found")
	except:
		print ("Fork search failed")
		forks = 'none'

	#search watch
	try:
		temp = re.search(r'"subscribers_count":\d+',s)
		temp1 = temp.group()
		watch = re.search(r'\d+',temp1)
		result = watch
	
		if result:
			print ("Watch number: "+result.group())
			watch = result.group()
		else:
			print ("Watch not found")
	except:
		print ("Watch search failed")
		watch = 'none'

	#search license
	try:
		temp = re.search(r'"license":.*?,"fork',s)
		temp1 = temp.group()
		#print (temp1)
		license = re.search(r'{.+}',temp1)
		
	
		if license:
			result = license
			if result:
				print ("License information: "+result.group())
				license = result.group()
				license_status = True
			else:
				print ("License = null")
		else:
			print ("License = null")
			license = 'null'
		
	except:
		print ("License search failed")
		license = 'none'

	result = requests.get('https://github.com'+user_repos)
	s = result.text
	s = str(s)
	
	
	#search contributors
	try:
		temp = re.search(r'\S+\s+</span>\s+contributor',s)
		if temp:
			temp1 = temp.group()
			#print (temp1)
			contributors = re.search(r'.*',temp1)
			result = contributors.group()
			result = result.strip()
		else:
			temp = re.search(r'>\S+</span>\s+contributors',s)
			if temp:
				temp1 = temp.group()
				contributors = re.search(r'>\S+<',temp1)
				result = contributors.group()
				result = result[1:-1]
				result = result.strip()
			else:
				temp = ''
				limit = retry_times
				while len(temp)==0:
					result = requests.get('https://api.github.com/repos'+user_repos+'/stats/contributors?access_token='+token+'&per_page=200')
					s = result.text
					s = str(s)
					temp = re.findall(r'"login":.*?"',s)
					print (len(temp))
					limit-=1
					if limit==0:
						limit = retry_times
						break
				if len(temp)==200:
					result = '200+'
				else:
					result = len(temp)
					result = str(result)
		if result:
			print ("Contributors number: "+result)
			contributors = result
		else:
			print ("Contributor search failed")
			contributors = '0'
	except:
		print ("Contributor search failed")
		contributors = 'none'


	#search commits
	result = requests.get('https://github.com'+user_repos)
	s = result.text
	s = str(s)
	try:
		temp = re.search(r'\S+\s+</span>\s+commit',s)
		temp1 = temp.group()
		#print (temp1)
		commits = re.search(r'.*',temp1)
		result = commits.group()
		#result = result.strip()
		if result:
			print ("Commits number: "+result)
			commits = result
		else:
			print ("Commit = 0")		
		
	except:
		print ("commit search failed")
		commits = 'none'
	
		
	#search commits in last year
	try:
		commit_week = ''
		limit = retry_times
		while len(commit_week)==0:
			result = requests.get('https://api.github.com/repos'+user_repos+'/stats/commit_activity?access_token='+token)
			s = result.text
			s = str(s)
			#print (s)
			commit_week = re.findall(r'"total":.*?,',s)
			print (len(commit_week))
			limit-=1
			if limit==0:
				limit = retry_times
				break
		
		if len(commit_week)!=0:
			commit_total = 0
			for i in range(len(commit_week)):
				t = commit_week[i][8:]
				#print (commit_week[i])
				t = t.replace(',','')
				#print (commit_week[i])
				commit_total = int(t)+commit_total
			#print (temp)
			print ("Commits number in last year:",commit_total)
			#print ("commit search failed")	
		else:
			print ("last year commit search failed")
			commit_total = 'none'
	except:
		print ("last year commit search failed")
		commit_total = 'none'
		
		
	#search latest commit
	result = requests.get('https://api.github.com/repos'+user_repos+'/commits/master?access_token=token')
	s = result.text
	s = str(s)
	#print (s)
	try:
		temp = re.search(r'"date":"\d+-\d+-\d+',s)
		if temp:
			temp1 = temp.group()
			#print (temp1)
			CommitDate = re.search(r'\d.*',temp1)
			CommitDate= CommitDate.group()
			#print (CommitDate)
			date = CommitDate[0:4]+CommitDate[5:7]+CommitDate[8:]
			LastDate = int(date)
		else:
			result = requests.get('https://api.github.com/repos'+user_repos+'/branches?access_token=token&per_page=60')
			s = result.text
			s = str(s)
			#print (s)
			temp = re.findall(r'"name":".*?"',s)
			#print (temp)
			for i in range(len(temp)):
				t = temp[i][8:]
				temp[i] = t.rstrip('"')
			Branch_list = temp
			#print (temp)
			LastDate = 0
			print ('Number of branches considered',len(Branch_list))
			for i in range(0,len(Branch_list)):
				result = requests.get('https://api.github.com/repos'+user_repos+'/commits/'+Branch_list[i]+'?access_token='+token)
				s = result.text
				s = str(s)
				#print (s)
				temp = re.search(r'"date":"\d+-\d+-\d+',s)
				temp1 = temp.group()
				#print (temp1)
				CommitDate = re.search(r'\d.*',temp1)
				CommitDate= CommitDate.group()
				#print (CommitDate)
				date = CommitDate[0:4]+CommitDate[5:7]+CommitDate[8:]
				date = int(date)
				#print (date)
				if date>LastDate:
					LastDate = date
					print (LastDate,i)		
			
		if result:
			print ("Latest commit date: ",LastDate,'\n')
			#CommitDate = result
		else:
			print ("Search error")
	except:
		print ("latest commit search failed")
		LastDate = 'none' 
	if star=='none' or forks=='none' or watch=='none' or license=='none' or contributors=='none' or commits=='none' or commit_total=='none' or LastDate=='none':
		failure_list.append(index)
	
	write_file(f,user_repos,index,star,forks,watch,license,contributors,commits,commit_total,LastDate)
	return failure_list
	
	
	
	

def read_url(path):
	f = open(path)
	url = f.read()
	r = re.findall(r'github.com/\S+/\S+ ',url)
	
	for i in range(len(r)):
		r[i] = r[i][10:]
		r[i] = r[i].rsplit('.git',1)
		r[i] = r[i][0] 
		r[i] = r[i].strip()
		r[i] = r[i].rstrip('/')
		#print (r)
	return r
#def pop_filter(star,forks,watch,license,commits,contributors,CommitDate):
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
