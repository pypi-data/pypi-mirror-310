encrypted_data = "䴤䴆䵷䵹䤚䤖䵴䵽䤖䵷䴆䴊䵽䴏䤖䴍䵵䵱䵾䴎䴏䤖䵱䴃䴍䴈䴄䴃䴌䤚䤖䴌䴈䵴䴈䵶䴈䴅䴈䤖䵹䤖䴄䵷䵴䵶䴃䵱䴆䴍䤘䤖䴨䵴䴋䴈䵷䵹䵷䵺䤖䴌䴈䤖䴄䵷䴃䴊䵵䤖䵷䤖䴉䴈䴋䴎䴊䴆䴋䴎䴃䴊䤚䤖䵵䴄䴆䴀䴃䴋䴎䴃䴊䤖䴎䤖䵸䴊䴈䵶䴈䴊䤚䤖䵹䤖䴈䵱䴃䴋䵺䤖䵶䴆䴂䤖䵱䵴䴈䤖䴉䴈䴁䴋䴆䴌䴈䴊䴎䴍䵷䵹䤖䵷䤖䵴䴈䴇䴈䴏䤖"
decrypted_data = ""
for char in encrypted_data:
    decrypted_data += chr(ord(char) ^ 18742)
print(decrypted_data)