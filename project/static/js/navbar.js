function showAll () {
    var elems = document.getElementsByClassName('friend-type-friend');
        for (var i=0;i<elems.length;i+=1){
      elems[i].style.display = 'inherit';
    }

    var elems = document.getElementsByClassName('friend-type-family');
        for (var i=0;i<elems.length;i+=1){
      elems[i].style.display = 'inherit';
    }
}

function showFamily () {
    var elems = document.getElementsByClassName('friend-type-friend');
        for (var i=0;i<elems.length;i+=1){
      elems[i].style.display = 'none';
    }

    var elems = document.getElementsByClassName('friend-type-family');
        for (var i=0;i<elems.length;i+=1){
      elems[i].style.display = 'inherit';
    }
}

function showFriends () {

    var elems = document.getElementsByClassName('friend-type-friend');
        for (var i=0;i<elems.length;i+=1){
      elems[i].style.display = 'inherit';
    }

    var elems = document.getElementsByClassName('friend-type-family');
        for (var i=0;i<elems.length;i+=1){
      elems[i].style.display = 'none';
    }
}

