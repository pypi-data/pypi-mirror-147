(Lib BAS) เป็นตัวอย่างการอัพโหลด package ไปยัง pypi.org
=======================================================

PyPi: https://pypi.org/project/lib_bas_eng/

สวัสดีจ้าาาา แพ็คนี้คือแพ็คเกจที่อธิบายโปรไฟล์ของนาย BAS
และสามารถนำไปใช้กับผู้อื่นได้

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install lib_bas_eng

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   from lib_bas_eng import BasInfo

   my = BasInfo('BAS')
   my.company = 'MIMO Tech'
   my.hobby = ['Play','Reading','Sleeping']
   print(my.name)
   my.show_email()
   my.show_myart()
   my.show_hobby()
   my.show_cat()
