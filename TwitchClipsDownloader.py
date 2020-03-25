'''
Created on March 24, 2020

@author: Tim
'''

#IF YOU GET THE VERSION OF WEBDRIVER ERROR, JUST REPLACE THE WEBDRIVER WITH THE VERSION OF YOUR CURRENT CHROME

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


import time
import urllib.request
import urllib
from tkinter import *
from tkinter import filedialog



newUrls = []
basepath='C:/Users/User/Downloads/'
out_filename = "Clip"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=r'C:\webdrivers\chromedriver.exe')
        
def on_closing():
    driver.close()
    driver.quit()
    window.destroy()
    Tk().destroy()

def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

def convert():
    textentry.update()
    text=textentry.get('1.0', END)
    text=str(text) 
    urls=text.splitlines()
    
    
    for x in range(len(urls)):
        if(x == 0):
            newUrls.clear()
        after = urls[x]
        after = after.replace("?filter=clips&range=30d&sort=time", "")
        after = after.replace("?filter=clips&range=7d&sort=time", "")
        after = after.replace("?filter=clips&range=24hr&sort=time", "")
        after = after.replace("?filter=clips&range=all&sort=time", "")
        streamer = after.replace("https://www.twitch.tv/", "")
        streamer = streamer.split("/")[0]
        after = after.replace("https://www.twitch.tv/" + streamer + "/clip/", "https://clips.twitch.tv/");
        newUrls.append(after)
       
    textentry.delete("1.0", END) #Clears textbox
    
    #Writes newUrls to the textbox
    for y in range(len(newUrls)):
        if y == len(newUrls) - 1:
            textentry.insert(y + 1.0, newUrls[y])
        else:
            textentry.insert(y + 1.0, newUrls[y] + "\n")
    
    download.config(state=NORMAL)

def download():
    
    for z in range(len(newUrls)):
        driver.get(newUrls[z])
        try:
            mp4 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"root\"]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div/div/video")))
            out_filename = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"root\"]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/span")))
            streamer_name = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"root\"]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[1]/div/div[1]/a/span")))
            time.sleep(3)
            
            reallink = mp4.get_attribute("src")
            out_filename = out_filename.text
            print(out_filename)
            
            textentry.insert(END, "\nDownloading " + (loctext.get() + streamer_name.text + "_" + out_filename + "_") + str(z + 1) + (".mp4") + "...")
            textentry.update()
        except:
            print("ERROR: Bad link- " + newUrls[z])
            textentry.insert(END, "\n\nERROR: Bad Link- " + newUrls[z])
            textentry.update()
            
        out_filename = out_filename.replace("?", "")
        out_filename = out_filename.replace("\\", "")
        out_filename = out_filename.replace("/", "")
        out_filename = out_filename.replace("*", "")
        out_filename = out_filename.replace(":", "")
        out_filename = out_filename.replace("\"", "")
        out_filename = out_filename.replace("<", "")
        out_filename = out_filename.replace(">", "")
        out_filename = out_filename.replace("|", "")
        
        output_path = (loctext.get() + streamer_name.text  + "_" + out_filename + "_") + str(z + 1) + (".mp4")
        urllib.request.urlretrieve(reallink, output_path, reporthook=dl_progress)
    
    textentry.insert(END, '\n\nFinished downloading all the videos.')
    
def location():
    basepath = filedialog.askdirectory()
    
    loctext.delete(0, "end")
    
    loctext.insert(0, basepath + "/")

##### main:
window = Tk()
window.title("Twitch Clips Downloader")
window.configure(background="black")
window.geometry("900x720")

#Title Label
Label (window, text="Enter twitch clips urls:", bg="black", fg="white", font="none 12 bold") .place(x=380, y=0, anchor="nw")

#Text Box
textentry = Text(window, width=120, height=40, bg ="#333333", fg="white", font="none 10")
textentry.place(x=30, y=30, anchor="nw")

#Buttons
convert = Button(window,text="CONVERT URL", width=20, command=convert) .place(x=50, y=685, anchor="nw")
download = Button(window,text="DOWNLOAD", width=20, state=DISABLED, command=download) 
download.place(x=230, y=685, anchor="nw")

#Location
Button(window,text="*", width=3, command=location) .place(x=595, y=685, anchor="nw")

#LocationText
loctext = Entry(window, bd=1, width=33)
loctext.insert(0, "C:/Users/User/Downloads/")
loctext.config(bg ="#333333", fg="grey", font="none 10 bold")
loctext.place(x=630, y=688, anchor="nw")

#####run the main loop
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()