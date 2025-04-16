import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ padding: 32, fontFamily: 'sans-serif', textAlign: 'center' }}>
      <img src="/logo.png" alt="Autom8Deals Logo" style={{ width: 160, marginBottom: 24 }} />
      <h1 style={{ color: '#0A2540', marginBottom: 8 }}>Autom8Deals</h1>
      <h2 style={{ color: '#FFB800', marginTop: 0, fontWeight: 400 }}>Automate. Earn. Repeat.</h2>
      <p style={{ maxWidth: 480, margin: '16px auto', color: '#222' }}>
        Welcome to your affiliate automation dashboard! Here you can monitor analytics, track site performance, and watch your network grow—all with zero manual effort.
      </p>
      <Link href="/analytics"><button style={{ marginRight: 12 }}>View Analytics</button></Link>
      <Link href="/onboarding"><button>Setup / Onboarding</button></Link>
    </div>
  );
}
