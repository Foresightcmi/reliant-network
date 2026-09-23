-- Run this in your Supabase SQL Editor

-- 1. Vendors Table (Contractors)
CREATE TABLE IF NOT EXISTS vendors (
  id TEXT PRIMARY KEY,
  niche_id TEXT NOT NULL,
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  phone TEXT,
  email TEXT,
  website TEXT,
  min_price NUMERIC,
  max_price NUMERIC,
  stripe_account_id TEXT,
  monopoly_active BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Leads Table
CREATE TABLE IF NOT EXISTS leads (
  id TEXT PRIMARY KEY,
  lead_code TEXT NOT NULL,
  niche_id TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  customer_name TEXT,
  customer_phone TEXT,
  customer_email TEXT,
  estimated_total NUMERIC,
  assigned_vendor_id TEXT REFERENCES vendors(id),
  status TEXT DEFAULT 'pending_dispatch', -- pending_dispatch, dispatched, claimed, expired
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
  expires_at TIMESTAMP WITH TIME ZONE
);

-- 3. Disable RLS for rapid MVP prototyping (WARNING: only for MVP)
ALTER TABLE vendors DISABLE ROW LEVEL SECURITY;
ALTER TABLE leads DISABLE ROW LEVEL SECURITY;
