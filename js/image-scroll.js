hs4Arr=[

["images/clients/cl-logo-1.png","","","images/clients/cl-logo-1.png"],
["images/clients/cl-logo-2.png","","","images/clients/cl-logo-2.png"],
["images/clients/cl-logo-3.png","","","images/clients/cl-logo-3.png"],
["images/clients/cl-logo-4.png","","","images/clients/cl-logo-4.png"],
["images/clients/cl-logo-5.png","","","images/clients/cl-logo-5.png"],
["images/clients/cl-logo-6.png","","","images/clients/cl-logo-6.png"],
["images/clients/cl-logo-7.png","","","images/clients/cl-logo-7.png"],
["images/clients/cl-logo-8.png","","","images/clients/cl-logo-8.png"],
["images/clients/cl-logo-9.png","","","images/clients/cl-logo-9.png"],
["images/clients/cl-logo-10.png","","","images/clients/cl-logo-10.png"],
["images/clients/cl-logo-11.png","","","images/clients/cl-logo-11.png"],
["images/clients/cl-logo-12.png","","","images/clients/cl-logo-12.png"],
["images/clients/cl-logo-13.png","","","images/clients/cl-logo-13.png"],
["images/clients/cl-logo-14.png","","","images/clients/cl-logo-14.png"],
["images/clients/cl-logo-15.png","","","images/clients/cl-logo-15.png"],
["images/clients/cl-logo-16.png","","","images/clients/cl-logo-16.png"],
["images/clients/cl-logo-17.png","","","images/clients/cl-logo-17.png"], 
["images/clients/cl-logo-18.png","","","images/clients/cl-logo-18.png"] 

// no comma at the end of last index

]

dir=0 // 0 = left 1 = right
speed=2
imageSize=100  // % set to zero to use fixedWidth and fixedHeight values
fixedWidth=0 // set a fixed width
fixedHeight=100// set a fixed height
spacerWidth=0 // space between images

alwaysCenter=1 // center the popup 0 = no 1 = yes
popupLeft=0 // popup default left, use if not centering
popupTop=0 // popup default top, use if not centering

biggest=0
ieBorder=0
totalWidth=0
hs4Timer=null

preload=new Array()
for(var i=0;i<hs4Arr.length;i++){
preload[i]=new Image()
preload[i].src=hs4Arr[i][0]
}

function initHS4(){
scroll1=document.getElementById("scroller1")

for(var j=0;j<hs4Arr.length;j++){

scroll1.innerHTML+='<img id="pic'+j+'" src="'+preload[j].src+'" onmouseover="this.src=\''+hs4Arr[j][3]+'\'" onmouseout="this.src=\''+preload[j].src+'\'" alt="'+hs4Arr[j][2]+'" title="'+hs4Arr[j][2]+'" onclick="showBigPic('+j+')">'

if(imageSize!=0){ // use percentage size
newWidth=preload[j].width/100*imageSize
newHeight=preload[j].height/100*imageSize
}
else{ // use fixed size
newWidth=fixedWidth
newHeight=fixedHeight
}

document.getElementById("pic"+j).style.width=newWidth+"px"
document.getElementById("pic"+j).style.height=newHeight+"px"

if(document.getElementById("pic"+j).offsetHeight>biggest){
biggest=document.getElementById("pic"+j).offsetHeight
}

document.getElementById("pic"+j).style.marginLeft=spacerWidth+"px"

totalWidth+=document.getElementById("pic"+j).offsetWidth+spacerWidth

}

totalWidth+=1

for(var k=0;k<hs4Arr.length;k++){ // vertically center images
document.getElementById("pic"+k).style.marginBottom = (biggest-document.getElementById("pic"+k).offsetHeight)/2+"px"
}

scrollBox=document.getElementById("scroll_box")

if(document.uniqueID && scrollBox.currentStyle && document.compatMode!="CSS1Compat"){
ieBorder=parseInt(scrollBox.currentStyle.borderWidth)*2
}

if(document.getElementById&&document.all){
ieBorder=parseInt(scrollBox.style.borderTopWidth)*2
}

scrollBox.style.height=biggest+ieBorder+"px"

scroll1.style.width=totalWidth+"px"

scroll2=document.getElementById("scroller2")
scroll2.innerHTML=scroll1.innerHTML
scroll2.style.left= scroll1.offsetWidth+"px"
scroll2.style.top= 0+"px"
scroll2.style.width=totalWidth+"px"

if(dir==1){
speed= -speed
}

scrollHS4()
}


function scrollHS4(){
if(paused==1){return}
clearTimeout(hs4Timer)

scroll1Pos=parseInt(scroll1.style.left)
scroll2Pos=parseInt(scroll2.style.left)

scroll1Pos-=speed
scroll2Pos-=speed

scroll1.style.left=scroll1Pos+"px"
scroll2.style.left=scroll2Pos+"px"

hs4Timer=setTimeout("scrollHS4()",30)

if(dir==0){
if(scroll1Pos< -scroll1.offsetWidth){
scroll1.style.left=scroll1.offsetWidth+"px"
}

if(scroll2Pos< -scroll1.offsetWidth){
scroll2.style.left=scroll1.offsetWidth+"px"
}
}

if(dir==1){
if(scroll1Pos>parseInt(scrollBox.style.width)){
scroll1.style.left=scroll2Pos+ (-scroll1.offsetWidth)+"px"
}

if(scroll2Pos>parseInt(scrollBox.style.width)){
scroll2.style.left=scroll1Pos+ (-scroll2.offsetWidth)+"px"
}
}

}

st=null
function pause(){
clearTimeout(hs4Timer)
clearTimeout(st)
}

function reStartHS4(){
clearTimeout(st)
st=setTimeout("scrollHS4()",100)
}

paused=0
picWin=null

function showBigPic(p){

if(hs4Arr[p][1]!=""){
paused=1

if(picWin&&picWin.open&&!picWin.closed){picWin.close()} // if picWin exists close it

if(hs4Arr[p][1].indexOf("png")!=-1){
bigImg=new Image()
bigImg.src=hs4Arr[p][1]

if(alwaysCenter==1){
popupLeft = (screen.availWidth - bigImg.width) / 2
popupTop = (screen.availHeight - bigImg.height) / 2
}

data="\n<center>\n<img src='"+bigImg.src+"'>\n<\/center>\n"

var winProps = "left= "+popupLeft+", top = "+popupTop+", width="+(bigImg.width+20)+", height="+(bigImg.height+20)+", scrollbars=no, toolbar=no, directories=no, menu bar=no, resizable=yes, status=no"

picWin=window.open("","win1",winProps)
picWin.document.write("<HTML>\n<HEAD>\n<TITLE><\/TITLE>\n")
picWin.document.write("<\/HEAD>\n")
picWin.document.write("<BODY style='background-color:black;margin-top:10px;margin-left:10px'>\n")
picWin.document.write("<div id=\"display\">"+data+"<\/div>")
picWin.document.write("\n<\/BODY>\n<\/HTML>")
}
else{
picWin=window.open(hs4Arr[p][1])
}

}

}

window.onfocus=function(){
paused=0
scrollHS4()
}

onunload=function(){ // close the popup when leaving page
if(picWin&&picWin.open&&!picWin.closed){
picWin.close()
}
}
