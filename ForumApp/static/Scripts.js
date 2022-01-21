function add_tag(){
var hidden = document.getElementById('tags_id');
var sel = document.getElementById('select_tag').selectedIndex;
var tag_field = document.getElementById('tags');
var elem = document.createElement('li');
if (sel > 0 && !hidden.value.includes('-'+sel+'-') && tag_field.childElementCount<5) {
hidden.value += sel+'-';
elem.textContent = document.getElementById('select_tag').options[sel].text;
elem.setAttribute('class','added_tag');
elem.setAttribute('name',sel);
elem.setAttribute('onclick','remove_tag(this)');
tag_field.appendChild(elem);
}
}
function remove_tag(elem){
var hidden = document.getElementById('tags_id');
var txt = hidden.value;
hidden.value = txt.replace('-'+elem.attributes['name'].value+'-','-');
elem.remove();
}