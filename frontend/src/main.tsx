import { StrictMode, useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { ArrowRight, CalendarDays, Check, Compass, Link2, MapPin, MessageCircle, RefreshCw, Sparkles, WalletCards } from 'lucide-react'
import { MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import './styles.css'

L.Icon.Default.mergeOptions({ iconRetinaUrl: markerIcon2x, iconUrl: markerIcon, shadowUrl: markerShadow })

type Pace = 'relaxed' | 'balanced' | 'packed'
type Activity = {
  id: string; name: string; category: string; description: string; neighborhood: string
  duration_hours: number; price_per_person: number; image: string; latitude: number; longitude: number
}
type Planned = {
  activity: Activity; slot: string; start_time: string; end_time: string
  travel_minutes_from_previous: number; score: number; reasons: string[]; alternatives: Activity[]
}
type Day = { day: number; date: string; theme: string; activities: Planned[]; estimated_cost: number; walking_km: number; total_hours: number }
type CostRow = { category: string; amount: number }
type Plan = {
  destination: string; destination_country: string; estimated_total: number; currency: string
  cost_breakdown: CostRow[]; days: Day[]; methodology: string[]; seasonal_note?: string | null
  ai_summary?: string | null; ai_enhanced?: boolean; unfilled_days: number[]
}

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const INTERESTS = ['Culture', 'Food', 'Outdoors', 'Wellness', 'History', 'Craft', 'Photography', 'Adventure']

const DESTINATION = {
  name: 'Shillong', label: 'Shillong, India', currency: 'INR', lodgingArea: 'Police Bazar',
  center: [25.5788, 91.8933] as [number, number], tagline: 'Shillong, at your own pace.',
}

const PRACTICAL_NOTES = [
  'No Inner Line Permit needed for Meghalaya (Indian citizens) — unlike some neighbouring Northeast states.',
  'Uber/Ola coverage is limited in Shillong — shared taxis and pre-booked cabs from Police Bazar are the norm.',
]

type TripParams = {
  originCity: string; startDate: string; endDate: string; travelers: number; travellerType: string
  budget: number; pace: Pace; interests: string[]; dietary: string[]; accessibility: boolean
}

function paramsFromSearch(search: string): TripParams | null {
  const query = new URLSearchParams(search)
  const startDate = query.get('start')
  const endDate = query.get('end')
  if (!startDate || !endDate) return null
  return {
    originCity: query.get('from') ?? 'Guwahati', startDate, endDate,
    travelers: Number(query.get('travelers') ?? 2), travellerType: query.get('type') ?? 'couple',
    budget: Number(query.get('budget') ?? 12000), pace: (query.get('pace') as Pace) ?? 'balanced',
    interests: (query.get('interests') ?? 'Outdoors,Culture').split(',').filter(Boolean),
    dietary: (query.get('dietary') ?? '').split(',').filter(Boolean),
    accessibility: query.get('accessibility') === '1',
  }
}

function searchFromParams(p: TripParams): string {
  const query = new URLSearchParams({
    from: p.originCity, start: p.startDate, end: p.endDate, travelers: String(p.travelers),
    type: p.travellerType, budget: String(p.budget), pace: p.pace, interests: p.interests.join(','),
    dietary: p.dietary.join(','), accessibility: p.accessibility ? '1' : '0',
  })
  return `${window.location.origin}${window.location.pathname}?${query.toString()}`
}

const CHERRAPUNJI_NEIGHBORHOOD = 'Cherrapunji (Sohra)'

function formatDate(value: string) {
  return new Intl.DateTimeFormat('en-US', { weekday: 'long', month: 'short', day: 'numeric' }).format(new Date(`${value}T12:00:00`))
}
function money(value: number, currency: string) {
  return new Intl.NumberFormat(currency === 'INR' ? 'en-IN' : 'en-US', { style: 'currency', currency, maximumFractionDigits: 0 }).format(value)
}

function DayMap({ day }: { day: Day }) {
  const points = day.activities.map((item) => [item.activity.latitude, item.activity.longitude] as [number, number])
  return (
    <MapContainer center={points[0] ?? DESTINATION.center} zoom={12} scrollWheelZoom={false} className="day-map">
      <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {points.length > 1 && <Polyline positions={points} pathOptions={{ color: '#bd5a42', weight: 3, dashArray: '2 8' }} />}
      {day.activities.map((item) => (
        <Marker key={item.activity.id} position={[item.activity.latitude, item.activity.longitude]}>
          <Popup>{item.activity.name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}

function App() {
  const [startDate, setStartDate] = useState('2026-11-10')
  const [endDate, setEndDate] = useState('2026-11-14')
  const [originCity, setOriginCity] = useState('Guwahati')
  const [travelers, setTravelers] = useState(2)
  const [travellerType, setTravellerType] = useState('couple')
  const [budget, setBudget] = useState(12000)
  const [pace, setPace] = useState<Pace>('balanced')
  const [interests, setInterests] = useState<string[]>(['Outdoors', 'Culture'])
  const [dietary, setDietary] = useState<string[]>([])
  const [accessibility, setAccessibility] = useState(false)
  const [plan, setPlan] = useState<Plan | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeDay, setActiveDay] = useState(0)
  const [swaps, setSwaps] = useState<Record<string, Activity>>({})
  const [linkCopied, setLinkCopied] = useState(false)

  const nights = useMemo(() => Math.max(1, Math.round((new Date(endDate).getTime() - new Date(startDate).getTime()) / 86400000)), [startDate, endDate])
  const toggleInterest = (interest: string) => setInterests((current) => current.includes(interest) ? current.filter((item) => item !== interest) : [...current, interest])

  const runPlan = async (p: TripParams) => {
    setLoading(true); setError(''); setSwaps({})
    try {
      const response = await fetch(`${API_URL}/api/plan`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origin_city: p.originCity, destination: DESTINATION.name, start_date: p.startDate, end_date: p.endDate,
          travelers: p.travelers, traveller_type: p.travellerType, budget: p.budget, currency: DESTINATION.currency,
          lodging_area: DESTINATION.lodgingArea, pace: p.pace, interests: p.interests,
          dietary_restrictions: p.dietary, accessibility: p.accessibility, enhance_with_ai: true,
        }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail ?? 'Could not generate a plan')
      setPlan(data)
      setActiveDay(0)
      window.history.replaceState(null, '', searchFromParams(p))
      setTimeout(() => document.getElementById('itinerary')?.scrollIntoView({ behavior: 'smooth' }), 50)
    } catch (err) {
      setError(err instanceof Error ? `${err.message}. Is the API running on port 8000?` : 'Something went wrong')
    } finally { setLoading(false) }
  }

  const generate = () => runPlan({ originCity, startDate, endDate, travelers, travellerType, budget, pace, interests, dietary, accessibility })

  useEffect(() => {
    const fromUrl = paramsFromSearch(window.location.search)
    if (!fromUrl) return
    setOriginCity(fromUrl.originCity); setStartDate(fromUrl.startDate); setEndDate(fromUrl.endDate)
    setTravelers(fromUrl.travelers); setTravellerType(fromUrl.travellerType); setBudget(fromUrl.budget)
    setPace(fromUrl.pace); setInterests(fromUrl.interests); setDietary(fromUrl.dietary); setAccessibility(fromUrl.accessibility)
    runPlan(fromUrl)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const swapActivity = (planId: string, alternative: Activity) => setSwaps((current) => ({ ...current, [planId]: alternative }))
  const displayedActivity = (item: Planned) => swaps[item.activity.id] ?? item.activity

  const copyShareLink = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href)
      setLinkCopied(true)
      setTimeout(() => setLinkCopied(false), 2000)
    } catch { /* clipboard permission denied; nothing to fall back to */ }
  }

  const shareOnWhatsApp = () => {
    if (!plan) return
    const message = `My ${nights}-night Shillong trip on Wishtrip (est. ${money(plan.estimated_total, plan.currency)}): ${window.location.href}`
    window.open(`https://wa.me/?text=${encodeURIComponent(message)}`, '_blank')
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#"><span className="brand-mark">W</span><span>WISHTRIP</span></a>
        <nav><a className="active" href="#planner">Plan a trip</a><a href="#how-it-works">How it works</a></nav>
        <button className="saved-button">♡ <span>Saved trips</span></button>
      </header>
      <main>
        <section className="hero" id="planner">
          <div className="hero-copy">
            <p className="eyebrow">A slower way to see the Northeast</p>
            <h1>Shillong, <em>at your own pace.</em></h1>
            <p className="hero-lede">Tell us what you love. We’ll shape a trip around it — with breathing room for the moments you can’t schedule.</p>
          </div>
          <div className="hero-stamp"><Sparkles size={15} /><span>CURATED FOR<br /><strong>YOUR RHYTHM</strong></span></div>
        </section>

        <section className="planner-card" aria-label="Trip preferences">
          <div className="card-heading">
            <div><span className="step">01</span><div><h2>Set your scene</h2><p>The essentials, then the little details.</p></div></div>
            <span className="destination-pill"><MapPin size={14} /> {DESTINATION.label}</span>
          </div>
          <ul className="practical-notes">{PRACTICAL_NOTES.map((note) => <li key={note}>{note}</li>)}</ul>
          <div className="form-grid">
            <label><span>FROM</span><div className="input-wrap"><MapPin size={16} /><input value={originCity} onChange={(event) => setOriginCity(event.target.value)} /></div></label>
            <label><span>CHECK IN</span><div className="input-wrap"><CalendarDays size={16} /><input type="date" value={startDate} onChange={(event) => setStartDate(event.target.value)} /></div></label>
            <label><span>CHECK OUT</span><div className="input-wrap"><CalendarDays size={16} /><input type="date" value={endDate} onChange={(event) => setEndDate(event.target.value)} /></div></label>
            <label><span>TRAVELERS</span><div className="input-wrap"><input type="number" min="1" max="12" value={travelers} onChange={(event) => setTravelers(Number(event.target.value))} /><small>people</small></div></label>
            <label><span>YOUR BUDGET</span><div className="input-wrap"><WalletCards size={16} /><input type="number" min="100" value={budget} onChange={(event) => setBudget(Number(event.target.value))} /><small>{DESTINATION.currency} total</small></div></label>
          </div>
          <div className="preferences-row">
            <div className="pace-control"><span className="label">TRIP STYLE</span><div className="segmented">{['solo', 'couple', 'family', 'friends', 'seniors'].map((value) => <button key={value} className={travellerType === value ? 'selected' : ''} onClick={() => setTravellerType(value)}>{value}</button>)}</div><span className="label">YOUR PACE</span><div className="segmented">{(['relaxed', 'balanced', 'packed'] as Pace[]).map((value) => <button key={value} className={pace === value ? 'selected' : ''} onClick={() => setPace(value)}>{value === 'relaxed' ? 'Slow & spacious' : value === 'balanced' ? 'A little of everything' : 'Make it count'}</button>)}</div></div>
            <div className="interest-control"><span className="label">I’M INTO</span><div className="chips">{INTERESTS.map((interest) => <button key={interest} className={interests.includes(interest) ? 'chip selected' : 'chip'} onClick={() => toggleInterest(interest)}>{interests.includes(interest) && <Check size={13} />}{interest}</button>)}</div></div>
          </div>
          <div className="extra-preferences"><label><span className="label">DIETARY</span><select value={dietary[0] ?? ''} onChange={(event) => setDietary(event.target.value ? [event.target.value] : [])}><option value="">No restriction</option><option value="vegetarian">Vegetarian</option><option value="vegan">Vegan</option></select></label><label className="check-option"><input type="checkbox" checked={accessibility} onChange={(event) => setAccessibility(event.target.checked)} /> Prefer accessible stops</label></div>
          <div className="generate-row"><span className="privacy-note">✦ No sign-up needed. Your preferences stay in this browser.</span><button className="primary-button" onClick={generate} disabled={loading}>{loading ? 'Finding your rhythm…' : 'Build my trip'} <ArrowRight size={17} /></button></div>
          {error && <p className="error-message">{error}</p>}
        </section>

        <section className="itinerary-section" id="itinerary">
          {loading && !plan ? (
            <div className="skeleton-list" aria-label="Building your itinerary">
              {[0, 1, 2].map((key) => <div className="skeleton-card" key={key}><div className="skeleton-line short" /><div className="skeleton-line" /><div className="skeleton-line" /></div>)}
            </div>
          ) : !plan ? <div className="empty-state"><Compass size={28} /><h2>Your Shillong story starts here.</h2><p>Set your preferences above and we’ll arrange a clear, considered itinerary in seconds.</p></div> : <>
            <div className="itinerary-header">
              <div><p className="eyebrow">YOUR PERSONAL ITINERARY</p><h2>{nights} nights in {plan.destination} <span>·</span> {travelers} {travelers === 1 ? 'traveler' : 'travelers'}</h2></div>
              <div className="header-actions">
                <div className="share-row">
                  <button className="share-button" onClick={copyShareLink}><Link2 size={13} /> {linkCopied ? 'Link copied!' : 'Copy link'}</button>
                  <button className="share-button" onClick={shareOnWhatsApp}><MessageCircle size={13} /> WhatsApp</button>
                </div>
                <div className="total-card"><span>EST. TRIP COST</span><strong>{money(plan.estimated_total, plan.currency)}</strong><small>of {money(budget, plan.currency)} budget · {plan.days.reduce((sum, day) => sum + day.walking_km, 0).toFixed(1)} km walking total</small></div>
              </div>
            </div>
            {plan.seasonal_note && <p className="seasonal-note"><Sparkles size={13} /> {plan.seasonal_note}</p>}
            {plan.unfilled_days.length > 0 && (
              <p className="unfilled-note">
                <Compass size={13} /> Day{plan.unfilled_days.length > 1 ? 's' : ''} {plan.unfilled_days.join(', ')} couldn’t be filled within your current filters — try relaxing your budget, dietary restrictions, or accessibility requirement.
              </p>
            )}
            <div className="itinerary-layout">
              <div className="day-list">
                {plan.days.map((day, index) => {
                  const isCherrapunjiDayTrip = day.activities.length > 1 && day.activities.every((item) => item.activity.neighborhood === CHERRAPUNJI_NEIGHBORHOOD)
                  return <article className="day-card" key={day.day}>
                  <div className="day-meta"><span className="day-number">DAY {String(day.day).padStart(2, '0')}</span><span>{formatDate(day.date)}</span><span className="theme">{day.theme}</span></div>
                  <div className="day-title-row"><h3>{day.day === 1 ? 'A gentle introduction' : day.day === 2 ? 'Waterfalls & tiny discoveries' : 'Follow your curiosity'} {isCherrapunjiDayTrip && <span className="day-trip-badge">🚗 Cherrapunji day trip</span>}</h3><span>{day.total_hours}h · {day.walking_km} km walking</span></div>
                  {day.activities.map((item) => {
                    const activity = displayedActivity(item)
                    return (
                      <div className="activity-row" key={item.activity.id}>
                        <img src={activity.image} alt="" />
                        <div className="activity-content">
                          <div className="activity-top">
                            <span className="slot">{item.slot}</span><span className="activity-time">{item.start_time} — {item.end_time}</span>
                            {item.travel_minutes_from_previous > 0 && <span className="travel-time">· {item.travel_minutes_from_previous} min from previous stop</span>}
                          </div>
                          <h4>{activity.name}</h4>
                          <p>{activity.description}</p>
                          <span className="reason"><Sparkles size={12} /> {item.reasons[0] ?? 'A strong fit for your trip'}</span>
                          {item.alternatives.length > 0 && (
                            <div className="swap-row">
                              {[item.activity, ...item.alternatives].filter((option) => option.id !== activity.id).map((option) => (
                                <button key={option.id} className="swap-button" onClick={() => swapActivity(item.activity.id, option)}>
                                  <RefreshCw size={11} /> Swap for {option.name}
                                </button>
                              ))}
                            </div>
                          )}
                        </div>
                        <span className="activity-price">{activity.price_per_person === 0 ? 'Free' : money(activity.price_per_person, plan.currency)}<small> / person</small></span>
                      </div>
                    )
                  })}
                  <button className={activeDay === index ? 'day-map-toggle open' : 'day-map-toggle'} onClick={() => setActiveDay(activeDay === index ? -1 : index)}>
                    <MapPin size={13} /> {activeDay === index ? 'Hide route map' : 'View route on map'}
                  </button>
                  {activeDay === index && <DayMap day={day} />}
                </article>
                })}
              </div>
              <aside className="methodology">
                <div className="aside-icon"><Sparkles size={16} /></div>
                <h3>Why this works for you</h3>
                {plan.ai_summary && <p className="ai-summary">{plan.ai_summary} <small>Claude-enhanced</small></p>}
                <p>Every stop is selected by a transparent planning engine — not a black box.</p>
                <ul>{plan.methodology.map((item) => <li key={item}><Check size={14} />{item}</li>)}</ul>
                {plan.cost_breakdown.length > 0 && (
                  <div className="cost-breakdown">
                    <span className="label">COST BREAKDOWN</span>
                    {plan.cost_breakdown.map((row) => {
                      const share = plan.estimated_total > 0 ? Math.round((row.amount / plan.estimated_total) * 100) : 0
                      return (
                        <div className="cost-row" key={row.category}>
                          <span>{row.category}</span>
                          <div className="cost-bar"><div style={{ width: `${share}%` }} /></div>
                          <span>{money(row.amount, plan.currency)}</span>
                        </div>
                      )
                    })}
                  </div>
                )}
              </aside>
            </div>
          </>}
        </section>
      </main>
      <footer><span>© 2026 Wishtrip</span><span>Made for more meaningful miles.</span><span>Shillong seed data · deterministic planning</span></footer>
    </div>
  )
}

export default App

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
