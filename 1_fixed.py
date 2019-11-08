import webbrowser
import time

i = 0
j = 1000
sessionToken = "HAyPFDzjnlbfmPjBaH3jGDoxNTUyMjU4MjAw"

fixed = "https://bugs.chromium.org/p/chromium/issues/csv?can=1&amp;num=1000&amp;q=status%3AFixed%20&amp;colspec=&amp;groupby=&amp;sort=&amp;start="
while i < 60:

	k = str(j)
	url = fixed+k+"&token="+sessionToken

	i = i + 1
	j = j + 1000

	webbrowser.open(url)
	time.sleep(10)

	
