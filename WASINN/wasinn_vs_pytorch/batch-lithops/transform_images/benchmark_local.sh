eval "$(conda shell.bash hook)"
conda activate python37


EXECUTIONS=2

realtimelist=()
for (( c=1; c<=$EXECUTIONS; c++ ))
do
   echo $c
   output=$( {  /bin/time -f "%e" python prepare-images.py ; } 2>&1 )

   real=$( echo "$output" | tail -n 1 )
   realtimelist+=("$real")

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


