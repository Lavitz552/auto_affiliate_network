import React, { useState } from 'react';

export default function Onboarding() {
  const [openaiKey, setOpenaiKey] = useState('');
  const [affiliateTag, setAffiliateTag] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // In production, send to backend API
    setSaved(true);
  };

  return (
    <div style={{ padding: 32, fontFamily: 'sans-serif' }}>
      <h1>Setup / Onboarding</h1>
      <p>Enter your API keys to get started:</p>
      <div>
        <label>OpenAI API Key:<br/>
          <input type="password" value={openaiKey} onChange={e => setOpenaiKey(e.target.value)} style={{ width: 300 }} />
        </label>
      </div>
      <div style={{ marginTop: 16 }}>
        <label>Amazon Affiliate Tag:<br/>
          <input type="text" value={affiliateTag} onChange={e => setAffiliateTag(e.target.value)} style={{ width: 300 }} />
        </label>
      </div>
      <button style={{ marginTop: 24 }} onClick={handleSave}>Save</button>
      {saved && <p style={{ color: 'green', marginTop: 12 }}>Saved! (For now, please also paste these into config.env)</p>}
    </div>
  );
}
