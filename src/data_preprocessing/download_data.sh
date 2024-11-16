#!/bin/bash

# Check if gsutil is available
if ! command -v gsutil &> /dev/null; then
  echo "gsutil not found. Please install Google Cloud SDK and authenticate first."
  exit 1
fi

# List of dish IDs you want to download
DISH_IDS=(
  1558459115
1558459276
1558549008
1558549773
1559678330
1559751801
1559838402
1559844506
1559844951
1559845290
1559846099
1560360055
1560368972
1560453174
1560453380
1560455030
1560527191
1560543755
1560973958
1560974707
1561061658
1561062555
1561392512
1561492204
1561575474
1561576590
1561580370
1561662054
1561662216
1561662458
1561665024
1561739238
1561739954
1561753238
1562008979
1562086702
1562094621
1562099053
1562183096
1562602860
1562611680
1562617703
1562618000
1562691032
1562691674
1562789268
1562862493
1562873028
1562873155
1562959732
1562963704
1563207364
1563216717
1563393217
1563468269
1563468299
1563468327
1563475921
1563476551
1563568338
1563813308
1563822597
1563824250
1563824339
1563898786
1563900150
1563984242
1563996485
1563998210
1563998323
1564000459
1564000490
1564082462
1565033110
1565033265
1565119464
1565119669
1565207815
1565383026
1565640549
1565725047
1565728415
1565972591
1566417398
1566417516
1566502505
1566502537
1566591080
1566838407
1566849327
1566849923
1566920365
1566938026
1567021831
1567106825
1567613057
1567628157
1568305257
1568314823
1568649312
)

# Create directories if they do not exist
mkdir -p data/raw/Nutrition5k/imagery/realsense_overhead
mkdir -p data/raw/Nutrition5k/imagery/side_angles
mkdir -p data/raw/Nutrition5k/metadata
mkdir -p data/raw/Nutrition5k/scripts

# Download the overhead images for the specified dish IDs
echo "Downloading overhead images..."
for dish_id in "${DISH_IDS[@]}"; do
  gsutil cp "gs://nutrition5k_dataset/nutrition5k_dataset/imagery/realsense_overhead/dish_${dish_id}/rgb.png" data/final/overhead/dish_${dish_id}/rgb.png
done

# Download the side-angle videos for the specified dish IDs
echo "Downloading side-angle videos..."
for dish_id in "${DISH_IDS[@]}"; do
  gsutil cp "gs://nutrition5k_dataset/nutrition5k_dataset/imagery/side_angles/dish_${dish_id}/camera_A.h264" data/raw//side_angle/dish_${dish_id}/camera_A.h264
done

# Download all metadata files
echo "Downloading metadata files..."
gsutil -m cp -r "gs://nutrition5k_dataset/nutrition5k_dataset/metadata/dish_metadata_cafe1.csv" data/raw/metadata/dish_metadata_cafe1.csv

# Download all scripts
echo "Downloading scripts..."
gsutil -m cp -r "gs://nutrition5k_dataset/nutrition5k_dataset/scripts/*" data/raw/scripts/

echo "All downloads complete!"