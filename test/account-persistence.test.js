import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';

const source = readFileSync(new URL('../server.js', import.meta.url), 'utf8');

function route(start, end, context = {}) {
  let handler;
  vm.runInNewContext(source.slice(source.indexOf(start), source.indexOf(end)), {
    Buffer,
    app: {
      post: (...args) => { handler = args.at(-1); },
      get: (...args) => { handler = args.at(-1); },
    },
    requireAuth() {},
    console: { log() {}, warn() {}, error() {} },
    ...context,
  });
  return handler;
}

function response() {
  return {
    statusCode: 200,
    status(value) { this.statusCode = value; return this; },
    json(value) { this.body = value; return this; },
  };
}

function verification(db) {
  return route("app.post('/api/auth/verify-code'", '// POST /api/auth/login', {
    db,
    crypto,
    codeAttempts: new Map(),
    verificationStore: new Map([['student@example.com', {
      code: '123456', expiresAt: Date.now() + 60000, used: false, issuedTo: 'unknown',
    }]]),
    getOrCreateUser: async () => ({ id: 7, name: null }),
    getUserPlan: async () => ({ plan: 'free', credits: 0 }),
    generateAuthToken: () => 'verified-session',
  });
}

test('returning users recover completion and name without a browser cache', async () => {
  const handler = verification({ query: async (sql) => ({
    rows: sql.includes('FROM onboarding') ? [{ full_name: 'Saved Student' }] : [{ id: 7 }],
  }) });
  const res = response();
  await handler({ body: { email: 'student@example.com', code: '123456' } }, res);
  assert.equal(res.statusCode, 200);
  assert.equal(res.body.onboarding_done, true);
  assert.equal(res.body.name, 'Saved Student');
  assert.equal(res.body.already_existed, true);
});

test('new accounts are sent to onboarding', async () => {
  const res = response();
  await verification({ query: async () => ({ rows: [] }) })(
    { body: { email: 'student@example.com', code: '123456' } }, res,
  );
  assert.equal(res.body.onboarding_done, false);
  assert.equal(res.body.already_existed, false);
});

test('a failed profile lookup never tells a returning user to repeat onboarding', async () => {
  const res = response();
  await verification({ query: async () => { throw new Error('database disconnected'); } })(
    { body: { email: 'student@example.com', code: '123456' } }, res,
  );
  assert.equal(res.statusCode, 503);
  assert.equal(res.body.token, undefined);
  assert.equal(res.body.onboarding_done, undefined);
});

test('onboarding cannot report success without database storage', async () => {
  const handler = route("app.post('/api/onboarding'", '//  PLAN & BILLING ROUTES', { db: null });
  const res = response();
  await handler({ body: { full_name: 'Student' }, userEmail: 'student@example.com' }, res);
  assert.equal(res.statusCode, 503);
  assert.equal(res.body.success, undefined);
});

test('onboarding cannot report success after a database write fails', async () => {
  const handler = route("app.post('/api/onboarding'", '//  PLAN & BILLING ROUTES', {
    db: { query: async () => { throw new Error('write failed'); } },
    getOrCreateUser: async () => ({ id: 7 }),
  });
  const res = response();
  await handler({ body: { full_name: 'Student' }, userEmail: 'student@example.com' }, res);
  assert.equal(res.statusCode, 500);
  assert.equal(res.body.success, undefined);
});

test('status lookup failures are explicit instead of a fabricated completion state', async () => {
  const handler = route("app.get('/api/onboarding/status'", '// POST /api/onboarding', {
    db: { query: async () => { throw new Error('read failed'); } },
    getOrCreateUser: async () => ({ id: 7 }),
  });
  const res = response();
  await handler({ userEmail: 'student@example.com' }, res);
  assert.equal(res.statusCode, 503);
  assert.equal(res.body.done, undefined);
});
