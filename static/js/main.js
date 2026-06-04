async function shortenURL() {
  const input = document.getElementById('urlInput');
  const result = document.getElementById('result');
  const url = input.value.trim();

  if (!url) {
    showResult('⚠️ Please enter a URL.', false);
    return;
  }

  try {
    const res = await fetch('/shorten', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const data = await res.json();

    if (data.short_code) {
      const shortLink = `${window.location.origin}/${data.short_code}`;
      showResult(`✅ Short URL: <a href="${shortLink}" target="_blank">${shortLink}</a>`, true);
      input.value = '';
      setTimeout(() => location.reload(), 1500);
    } else {
      showResult('❌ ' + (data.error || 'Something went wrong'), false);
    }
  } catch (err) {
    showResult('❌ Server error. Is Flask running?', false);
  }
}

function showResult(msg, success) {
  const result = document.getElementById('result');
  result.innerHTML = msg;
  result.className = 'result' + (success ? '' : ' error');
}

async function deleteURL(id) {
  if (!confirm('Delete this URL?')) return;

  try {
    const res = await fetch(`/delete/${id}`, { method: 'DELETE' });
    if (res.ok) {
      document.getElementById(`row-${id}`).remove();
    }
  } catch (err) {
    alert('Delete failed.');
  }
}

document.getElementById('urlInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') shortenURL();
});