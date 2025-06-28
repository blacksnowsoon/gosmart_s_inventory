const footer_content = 
`<div class="navbar fixed-bottom navbar-default border-top">
  <div class="container">
    <div>
      <small class="">Simple Inventory Management Version 1.0.0</small><br>
      
    </div>
    <div><small class="">© 2025 GO Smart Soultion. All rights reserved.</small></div>
  </div>
  </div>`;

  $('footer').html(footer_content);

  // spenner
function spenner(){
  const container = document.createElement('div');
  container.classList.add('d-flex');
  container.classList.add('justify-content-center');
	const spenner = document.createElement('div');
	spenner.classList.add('text-center');
	spenner.classList.add('spinner-grow');
	spenner.classList.add('text-info');
	spenner.classList.add('spinner-border-sm');
	spenner.classList.add('mb-3');
	spenner.setAttribute('role', 'status');
	spenner.setAttribute('aria-hidden', 'true');
  container.appendChild(spenner);
	return container
}