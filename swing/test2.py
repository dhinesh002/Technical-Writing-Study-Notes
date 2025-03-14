

for i in range(0, 10):
    print(i)

# in php 
"""
<?php
for ($i = 0; $i < 10; $i++) {
    echo $i . "\n";
}
?>
"""
# -------------------------------------

letters = ['a', 'b']
for letter in letters:
    print(letter)

""" 
<? php 
$letters = ['a', 'b']

foreach($letters as $letter){
    echo $letter
} 
?>  

  """


letters = ['a', 'b']
for index, item in enumerate(letters):
    print(item)

"""
<?php 
$letters = ['a', 'b'];

foreach ($letters as $index => $item) {
    echo $index . ": " . $item . "\n";
} 
?> 

"""   


dic = {"name": 'dhin', 'age': 20}

for key , item in dic.items():
    print(key)


