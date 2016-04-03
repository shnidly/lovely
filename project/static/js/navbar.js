function navbar () {
	alert("here");

	var input = `<ul class="sidebar-menu" id="nav">
                    <li class="active">
                      <a class="" href="index.html">
                          <span>Person 1</span>
                          <span class="glyphicon glyphicon-heart" style="color: #462066"></span>
                      </a>
                  </li>
                  <li class="sub-menu">
                      <a href="javascript:;" class="">
                          <span>Person 2</span>
                      </a>
                  </li>

                  <li class="sub-menu">
                      <a href="javascript:;" class="">
                          <span>Person 3</span>
                      </a>
                  </li>
                  </ul>
                  <div id="plus">

                  <a href="#"><div class="round-button" alt="add contact"><span class="glyphicon glyphicon-plus"></span></div></a>
              </div>`;

 document.getElementById("nav").innerHTML = input;
 }