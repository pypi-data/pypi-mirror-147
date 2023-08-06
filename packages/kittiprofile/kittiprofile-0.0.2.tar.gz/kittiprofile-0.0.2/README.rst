(Kitti Profile) เป็นตัวอย่างการอัพโหลด Package ไปยัง pypi.org
=============================================================

PyPi: https://pypi.org/project/kittiprofile/

เป็น Package ที่อธิบาย Profile ส่วนตัว

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install kittiprofile

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   my = Profile('Kong')
   my.company = 'PSU'
   my.hobby = ['Fishing ','Running','Sleeping']
   print(my.name)
   my.show_email()
   my.show_myart()
   my.show_hobby()
   my.show_gandalf()

