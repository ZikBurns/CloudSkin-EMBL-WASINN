eval "$(conda shell.bash hook)"
conda activate python37

EXECUTIONS=10

realtimelist=()
for (( c=1; c<=$EXECUTIONS; c++ ))
do
   echo $c
   output=$( { time python main.py ; } 2>&1 )

   real=$( echo "$output" | grep real )
   real=$(echo $real | grep -oP '\d+m\d+,\d+s' | sed 's/m//;s/,/./;s/s$//' | bc)
   realtimelist+=("$real")

   user=$( echo "$output" | grep user )
   user=$(echo $user | grep -oP '\d+m\d+,\d+s' | sed 's/m//;s/,/./;s/s$//' | bc)
   userrealtimelist+=("$user")

   sys=$( echo "$output" | grep sys )
   sys=$(echo $sys | grep -oP '\d+m\d+,\d+s' | sed 's/m//;s/,/./;s/s$//' | bc)
   sysrealtimelist+=("$sys")
done
echo "Real times: ${realtimelist[@]}"
sum=0
sum_squares=0
for onetime in ${realtimelist[@]}; do
   sum=$(echo "$sum + $onetime" | bc)
   sum_squares=$(echo "$sum_squares + $onetime^2" | bc)
done
echo "Real total time: $sum"
count=${#realtimelist[@]}
average=$(echo "scale=3; $sum / $count" | bc)
echo "Real Avg time: $average"

variance=$(echo "scale=2; $sum_squares / $count - ($average^2)" | bc)
if [ $(echo "$variance < 0" | bc -l) -eq 1 ]
then
  standard_deviation=0
else
  standard_deviation=$(echo "scale=2; sqrt($variance)" | bc)
fi
echo "Real Standard deviation: $standard_deviation"

echo "#########################################"
echo "User times: ${userrealtimelist[@]}"
sum=0
sum_squares=0
for onetime in ${userrealtimelist[@]}; do
   sum=$(echo "$sum + $onetime" | bc)
   sum_squares=$(echo "$sum_squares + $onetime^2" | bc)
done
echo "User total time: $sum"
count=${#userrealtimelist[@]}
average=$(echo "scale=3; $sum / $count" | bc)
echo "User avg time is : $average"

variance=$(echo "scale=2; $sum_squares / $count - ($average^2)" | bc)
if [ $(echo "$variance < 0" | bc -l) -eq 1 ]
then
  standard_deviation=0
else
  standard_deviation=$(echo "scale=2; sqrt($variance)" | bc)
fi
echo "User standard deviation:$standard_deviation"


echo "#########################################"
echo "Sys times: ${sysrealtimelist[@]}"
sum=0
sum_squares=0
for onetime in ${sysrealtimelist[@]}; do
   sum=$(echo "$sum + $onetime" | bc)
   sum_squares=$(echo "$sum_squares + $onetime^2" | bc)
done
echo "Sys total time: $sum"
count=${#sysrealtimelist[@]}
average=$(echo "scale=3; $sum / $count" | bc)
echo "Sys avg time is : $average"

variance=$(echo "scale=2; $sum_squares / $count - ($average^2)" | bc)
if [ $(echo "$variance < 0" | bc -l) -eq 1 ]
then
  standard_deviation=0
else
  standard_deviation=$(echo "scale=2; sqrt($variance)" | bc)
fi
echo "Sys standard deviation:$standard_deviation"

