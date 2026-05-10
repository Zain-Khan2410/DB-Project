// ─── CSRF helper ─────────────────────────────────────────────────────────────
function getCookie(name) {
  let value = null;
  if (document.cookie) {
    document.cookie.split(';').forEach(c => {
      const [k, v] = c.trim().split('=');
      if (k === name) value = decodeURIComponent(v);
    });
  }
  return value;
}

const CSRF = getCookie('csrftoken');

// ─── Update cart badge on load ────────────────────────────────────────────────
function updateCartBadge(count) {
  const badge = document.getElementById('cart-badge');
  if (!badge) return;
  if (count !== undefined) {
    badge.textContent = count;
  }
  const currentCount = parseInt(badge.textContent || '0');
  badge.style.display = currentCount > 0 ? 'flex' : 'none';
}

// ─── Add to Cart ─────────────────────────────────────────────────────────────
function addToCart(itemId, button) {
  const qtyEl = document.getElementById(`qty-${itemId}`);
  const quantity = qtyEl ? parseInt(qtyEl.textContent) : 1;

  fetch('/orders/cart/add/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF },
    body: JSON.stringify({ item_id: itemId, quantity: quantity }),
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      updateCartBadge(data.cart_count);
      // Animate button
      if (button) {
        const orig = button.innerHTML;
        button.innerHTML = '✓ Added!';
        button.style.background = '#48BB78';
        setTimeout(() => {
          button.innerHTML = orig;
          button.style.background = '';
        }, 1500);
      }
      showToast('Item added to cart!', 'success');
    } else {
      showToast(data.message || 'Could not add item.', 'error');
    }
  })
  .catch(() => showToast('Network error.', 'error'));
}

// ─── Update Cart (inline) ─────────────────────────────────────────────────────
function updateCart(itemId, action) {
  fetch('/orders/cart/update/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF },
    body: JSON.stringify({ item_id: itemId, action: action }),
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) location.reload();
  });
}

// ─── Quantity Controls ────────────────────────────────────────────────────────
function changeQty(itemId, delta) {
  const el = document.getElementById(`qty-${itemId}`);
  if (!el) return;
  let val = parseInt(el.textContent) + delta;
  if (val < 1) val = 1;
  if (val > 99) val = 99;
  el.textContent = val;
}

// ─── Toast Notification ───────────────────────────────────────────────────────
function showToast(message, type = 'info') {
  const existing = document.getElementById('toast-container');
  if (existing) existing.remove();

  const container = document.createElement('div');
  container.id = 'toast-container';
  container.style.cssText = `
    position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;
  `;

  const toast = document.createElement('div');
  const colors = { success: '#48BB78', error: '#FC8181', info: '#63B3ED', warning: '#F6AD55' };
  toast.style.cssText = `
    background: ${colors[type] || colors.info};
    color: white; padding: 0.85rem 1.5rem;
    border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    font-family: Poppins, sans-serif; font-size: 0.9rem; font-weight: 500;
    animation: slideUp 0.3s ease; max-width: 300px;
  `;
  toast.textContent = message;

  const style = document.createElement('style');
  style.textContent = '@keyframes slideUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }';
  document.head.appendChild(style);

  container.appendChild(toast);
  document.body.appendChild(container);
  setTimeout(() => container.remove(), 3000);
}

// ─── Auto-dismiss alerts ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  updateCartBadge();

  // Auto-dismiss messages after 4 seconds
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.4s';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });
});
