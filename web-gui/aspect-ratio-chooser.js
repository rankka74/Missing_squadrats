(function() {
	var activeRatio = [16, 9];
	var rotated = false;

	var chooser = document.createElement('div');
	chooser.id = 'ar-chooser';
	chooser.innerHTML = ""
		+ '<span class="ar-label">Aspect ratio</span>'
		+ '<div class="ar-presets">'
		+ '  <button class="ar-btn" data-w="1" data-h="1">1:1</button>'
		+ '  <button class="ar-btn" data-w="4" data-h="3">4:3</button>'
		+ '  <button class="ar-btn active" data-w="16" data-h="9">16:9</button>'
		+ '</div>'
		+ '<div class="ar-divider"></div>'
		+ '<button class="ar-rotate-btn" id="ar-rotate" title="Rotate (swap width and height)">'
		+ '  <i class="ar-rotate-icon">⇄</i> Rotate'
		+ '</button>'
		+ '<div class="ar-divider"></div>'
		+ '<div class="ar-custom">'
		+ '  <input type="number" id="ar-cw" min="1" max="999" value="16" title="Width ratio">'
		+ '  <span class="ar-sep">:</span>'
		+ '  <input type="number" id="ar-ch" min="1" max="999" value="9" title="Height ratio">'
		+ '  <button id="ar-apply">Apply</button>'
		+ '</div>'
		+ '<span class="ar-display" id="ar-info"></span>';

	var mapEl = document.getElementById('map');
	mapEl.parentNode.insertBefore(chooser, mapEl);

	function setMapHeight(px) {
		mapEl.style.setProperty('height', px + 'px', 'important');
		if (window.map && typeof window.map.invalidateSize === 'function') {
			setTimeout(function() { window.map.invalidateSize(); }, 60);
		}
	}

	function getContainerWidth() {
		mapEl.style.setProperty('width', '100%', 'important');
		return mapEl.offsetWidth || 940;
	}

	function applyRatio(w, h) {
		activeRatio = [w, h];
		var rw = rotated ? h : w;
		var rh = rotated ? w : h;
		var width = getContainerWidth();
		var height = Math.round(width * rh / rw);
		var maxHeight = Math.floor(window.innerHeight * 0.8);
		if (height > maxHeight) {
			height = maxHeight;
			width = Math.round(height * rw / rh);
			mapEl.style.setProperty('width', width + 'px', 'important');
		}
		setMapHeight(height);
		var info = document.getElementById('ar-info');
		if (info) {
			info.innerHTML = '<strong>' + rw + ':' + rh + '</strong>&nbsp; '
				+ width + '&thinsp;×&thinsp;' + height + '&thinsp;px';
		}
	}

	function syncCustomInputs(w, h) {
		var rw = rotated ? h : w;
		var rh = rotated ? w : h;
		document.getElementById('ar-cw').value = rw;
		document.getElementById('ar-ch').value = rh;
	}

	function setActive(btn) {
		chooser.querySelectorAll('.ar-btn').forEach(function(b) { b.classList.remove('active'); });
		if (btn) btn.classList.add('active');
	}

	chooser.querySelectorAll('.ar-btn').forEach(function(btn) {
		btn.addEventListener('click', function() {
			setActive(btn);
			applyRatio(+btn.dataset.w, +btn.dataset.h);
			syncCustomInputs(+btn.dataset.w, +btn.dataset.h);
		});
	});

	document.getElementById('ar-rotate').addEventListener('click', function() {
		rotated = !rotated;
		this.classList.toggle('active', rotated);
		applyRatio(activeRatio[0], activeRatio[1]);
		syncCustomInputs(activeRatio[0], activeRatio[1]);
	});

	function applyCustom() {
		var cw = parseInt(document.getElementById('ar-cw').value, 10);
		var ch = parseInt(document.getElementById('ar-ch').value, 10);
		if (!cw || !ch || cw < 1 || ch < 1) return;
		var sw = rotated ? ch : cw;
		var sh = rotated ? cw : ch;
		var match = null;
		var buttons = chooser.querySelectorAll('.ar-btn');
		for (var i = 0; i < buttons.length; i++) {
			if (+buttons[i].dataset.w === sw && +buttons[i].dataset.h === sh) {
				match = buttons[i];
				break;
			}
		}
		setActive(match);
		activeRatio = [sw, sh];
		var width = getContainerWidth();
		var height = Math.round(width * ch / cw);
		var maxHeight = Math.floor(window.innerHeight * 0.8);
		if (height > maxHeight) {
			height = maxHeight;
			width = Math.round(height * cw / ch);
			mapEl.style.setProperty('width', width + 'px', 'important');
		}
		setMapHeight(height);
		var info = document.getElementById('ar-info');
		if (info) {
			info.innerHTML = '<strong>' + cw + ':' + ch + '</strong>&nbsp; '
				+ width + '&thinsp;×&thinsp;' + height + '&thinsp;px';
		}
	}

	document.getElementById('ar-apply').addEventListener('click', applyCustom);
	['ar-cw', 'ar-ch'].forEach(function(id) {
		document.getElementById(id).addEventListener('keydown', function(e) {
			if (e.key === 'Enter') applyCustom();
		});
	});

	window.addEventListener('resize', function() {
		applyRatio(activeRatio[0], activeRatio[1]);
	});

	applyRatio(16, 9);
})();
