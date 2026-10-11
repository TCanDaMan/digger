// Paste into the browser console on https://www.rottentomatoes.com/m/digger_2026/reviews
// Resumes the critic-review download at page 6 ('Ng==' = base64 "6").
// If it stops with a 401, wait a minute, set `after` to the cursor it printed, and run again.
(async () => {
  const id = '6e03a6b1-1dce-32fd-84b1-6e74b3d040bd', out = [];
  let after = 'Ng==';
  for (let i = 0; i < 20; i++) {
    const r = await fetch(`/napi/rtcf/v1/movies/${id}/reviews?after=${encodeURIComponent(after)}&before=&pageCount=20&topOnly=false&type=critic&verified=false`);
    if (!r.ok) { console.warn('stopped at cursor', after, 'status', r.status); break; }
    const j = await r.json();
    for (const v of j.reviews || []) out.push({ id: v.reviewId, critic: v.critic?.displayName, outlet: v.publication?.name, top: v.critic?.isTopCritic, fresh: v.scoreSentiment, score: v.originalScore ?? null, date: v.createDate?.slice(0, 10), url: v.publicationReviewUrl });
    console.log('cursor', after, 'total', out.length);
    if (!j.pageInfo?.hasNextPage) break;
    after = j.pageInfo.endCursor;
    await new Promise(r => setTimeout(r, 4000));
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out)], { type: 'application/json' }));
  a.download = 'digger_rt_reviews_part2.json'; document.body.appendChild(a); a.click(); a.remove();
  console.log(`Done: ${out.length} more reviews saved`);
})();
