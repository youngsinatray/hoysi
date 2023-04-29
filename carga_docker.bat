
@REM Uploading docker image to DockerHub  
docker build -t youngsinatra/hoysi . 
docker push youngsinatra/hoysi:latest

@REM Pushing to repo chages (the ones in .github/ are the ones that matters)
git add .
git commit -m "[~] Changed schedule, second try"
git push

@REM git config --global user.name youngsinatray
@REM git config --global user.email ohzhink@gmail.com