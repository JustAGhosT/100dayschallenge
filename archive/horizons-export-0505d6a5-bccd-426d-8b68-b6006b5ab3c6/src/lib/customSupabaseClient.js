import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://cdpblhrojfnqbaemkkzn.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkcGJsaHJvamZucWJhZW1ra3puIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0NDE0NDIsImV4cCI6MjA2MTAxNzQ0Mn0.e5hYmbzxH6gYTi2sDiH_nF0o9VUI5E35WLyWsjWu4Pc';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);