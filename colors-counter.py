from PIL import Image, ImageDraw

if len (sys.argv) > 1:
        im1 = Image.open(sys.argv[-1]).convert("P")
        im = im1.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        FileName = "count.txt"
        PictPal = im.getpalette()
        ColorsNum = im.getcolors()
        with open(FileName, "w") as file:
                file.write('Number of colors in image = ' + str(len(ColorsNum))+"\n\n")
        n=0
        for i in range (len(ColorsNum)):
                text = ColorsNum[i]
                color = (PictPal[n+0], PictPal[n+1], PictPal[n+2])
                with open(FileName, "a") as file:
                        file.write(str(text[0])+" ")
                        file.write(str(color)+"\n")
                img = Image.new('RGB', (130, 50), color)
                imgDrawer = ImageDraw.Draw(img)
                imgDrawer.text((20, 20), 'color '+str(i)+' - '+str(text[0]), fill=(120,120,120))
                img.save("color_0"+str(i)+".png")
                n+=3
        with open(FileName, "a") as file:
                file.write("\n-----------------------------------\n")
                file.write("image colors counter by nodeus ©2018")
else:
        print ("Нет аргументов! Вызов должен быть в формате color-conter.exe image.png")