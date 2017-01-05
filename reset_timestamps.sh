for file in `git ls-files`; do
	echo $file
	touch -d "$(git log --pretty=format:%ai -n1 "$file")" $file
done
