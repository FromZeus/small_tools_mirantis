except()
{
  case "$1" in
    -n)
      echo "-n There have to be a parameter value - name of the package"
      exit 1
      ;;
  esac
}

main()
{
  for el in $(yum list)
    do
      if [[ $el != *"base"* && $el != *"epel"* && 
        $el != *"extras"* && $el != *"updates"* && 
        $el != *"el7"* && $el != *"fc23"* ]]
        then
          res=$(repoquery --requires $el | grep $package_name)
          if [[ $res != "" ]]
            then
              echo -e "$el depends on $res\n"
          fi
      fi
    done
}

while [ $# -gt 0 ]
do
  case "$1" in 
    -n)
      shift
      if [ $# -gt 0 ]
        then
          package_name="$1"
        else
          except -n
      fi
      shift
      ;;
  esac
done

if [[ $package_name == "" ]]
  then
    exit 1
fi

cur_time=$(date -R)
echo "Searching for dependency $package_name started at 
  $cur_time"
main
cur_time=$(date -R)
echo "Searching for dependency $package_name finished at 
  $cur_time"