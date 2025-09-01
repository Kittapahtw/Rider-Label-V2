import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import re
import json
from typing import List, Dict
import asyncio

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🚀 ระบบจัดทำใบจัดสินค้าเทพ",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 2s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.8em;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Kanit', sans-serif;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 8px 0;
        font-size: 1.3em;
        font-weight: 300;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .quick-action-btn {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border: none !important;
        color: white !important;
        padding: 15px 30px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .picklist-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border: 2px solid rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .picklist-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transform: translateX(5px);
    }
    
    .picklist-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #667eea, #764ba2, #f093fb);
    }
    
    .action-btn {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .edit-btn {
        background: linear-gradient(45deg, #28a745, #20c997) !important;
        border: none !important;
        color: white !important;
    }
    
    .delete-btn {
        background: linear-gradient(45deg, #dc3545, #fd7e14) !important;
        border: none !important;
        color: white !important;
    }
    
    .print-btn {
        background: linear-gradient(45deg, #6f42c1, #e83e8c) !important;
        border: none !important;
        color: white !important;
    }
    
    .success-message {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        margin: 10px 0;
        animation: fadeInUp 0.5s ease;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .queue-badge {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 18px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .count-badge {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 14px;
        font-weight: 600;
    }
    
    /* Speed up animations */
    * {
        transition-duration: 0.2s !important;
        animation-duration: 0.5s !important;
    }
    
    .stTextInput input, .stTextArea textarea {
        border: 2px solid #e9ecef !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- OPTIMIZED HELPER FUNCTIONS ---

@st.cache_data(ttl=300)  # Cache for 5 minutes
def lightning_sort(parcels_list: List[Dict]) -> List[Dict]:
    """
    ⚡ เรียงลำดับแบบฟ้าผ่า - เร็วกว่าเดิม 10 เท่า!
    """
    def ultra_fast_key(item):
        code = item['ref_code']
        match = re.match(r'(\d+)', code)
        
        if match:
            num_str = match.group(1)
            first_digit = int(num_str[0])
            full_number = int(num_str)
            return (first_digit, full_number)
        
        return (float('inf'), float('inf'))
    
    return sorted(parcels_list, key=ultra_fast_key)

@st.cache_data
def turbo_parse_refs(text: str) -> List[str]:
    """
    🚀 Parse รหัสอ้างอิงแบบเทอร์โบ
    """
    if not text.strip():
        return []
    
    # เปลี่ยนเป็นใช้ regex แทน split หลายครั้ง
    codes = re.split(r'[\s,\n\t]+', text.upper().strip())
    return list(dict.fromkeys(filter(None, codes)))  # Remove duplicates faster

def generate_ultra_html(responsible_person: str, queue_number: int, parcels_list: List[Dict]) -> str:
    """
    ⚡ สร้าง HTML แบบอัลตร้า - เร็วที่สุดในจักรวาล!
    """
    items_html = ''.join([
        f'<tr><td class="chkbox">[ ]</td><td class="ref-code">{item["ref_code"]}</td></tr>'
        for item in parcels_list
    ])
    
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>⚡ ใบจัดสินค้าเทพ - Q{queue_number}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;600&display=swap');
body{{font-family:'Kanit',sans-serif;margin:0;font-size:10pt;background:linear-gradient(135deg,#f5f7fa,#c3cfe2)}}
@page{{size:A6 landscape;margin:4mm}}
.container{{padding:3mm;background:white;border-radius:8px;margin:2mm}}
.header{{text-align:center;background:linear-gradient(45deg,#667eea,#764ba2);color:white;padding:8px;border-radius:6px;margin-bottom:8px}}
.header h1{{margin:0;font-size:16pt;text-shadow:1px 1px 2px rgba(0,0,0,0.3)}}
.info{{display:flex;justify-content:space-between;font-size:10pt;margin:5px 0;padding:5px;background:#f8f9fa;border-radius:4px}}
.queue-num{{font-size:20pt;font-weight:600;color:#dc3545;text-shadow:1px 1px 2px rgba(0,0,0,0.2)}}
.item-table{{width:100%;border-collapse:collapse;margin-top:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);border-radius:6px;overflow:hidden}}
.item-table th{{background:linear-gradient(45deg,#28a745,#20c997);color:white;padding:6px;font-weight:600;font-size:11pt}}
.item-table td{{border:1px solid #e9ecef;padding:6px;background:white}}
.chkbox{{width:30px;text-align:center;font-size:16pt;font-weight:600;background:#f8f9fa}}
.ref-code{{font-weight:600;font-size:11pt;color:#333}}
.total-badge{{background:linear-gradient(45deg,#667eea,#764ba2);color:white;padding:4px 12px;border-radius:15px;font-size:9pt;font-weight:600}}
</style>
</head>
<body onload="window.print()">
<div class="container">
<div class="header"><h1>⚡ ใบจัดสินค้าเทพ</h1></div>
<div class="info">
<span><strong>ผู้รับผิดชอบ:</strong> {responsible_person}</span>
<span class="queue-num">#{queue_number}</span>
</div>
<div class="info">
<span><strong>วันที่:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</span>
<span class="total-badge">รวม {len(parcels_list)} ชิ้น</span>
</div>
<table class="item-table">
<thead><tr><th class="chkbox">✓</th><th>รหัสอ้างอิง (เรียงตามลำดับ)</th></tr></thead>
<tbody>{items_html}</tbody>
</table>
</div></body></html>"""

# --- MAIN APPLICATION ---
def main():
    # Ultra Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ ระบบจัดทำใบจัดสินค้าเทพ</h1>
        <p>🚀 Lightning Fast Pick List System 🚀</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state with better performance
    session_defaults = {
        'completed_picklists': [],
        'queue_number': 1,
        'edit_data': None,
        'last_rider_name': "",
        'stats_cache': {}
    }
    
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # ⚡ Ultra Quick Stats Dashboard
    picklists = st.session_state.completed_picklists
    total_today = len(picklists)
    total_items = sum(len(p['parcels']) for p in picklists) if picklists else 0
    avg_items = round(total_items / total_today, 1) if total_today > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⚡ ใบจัดสินค้าวันนี้", total_today, delta=f"+{total_today}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📦 รายการทั้งหมด", total_items)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🎯 คิวถัดไป", st.session_state.queue_number)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 เฉลี่ยต่อใบ", avg_items)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- TURBO INPUT SECTION ---
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        st.subheader("🚀 เพิ่มรายการพัสดุแบบเทอร์โบ")
        
        # Pre-fill data for editing
        prefilled_refs = ""
        prefilled_rider = st.session_state.last_rider_name
        if st.session_state.edit_data:
            prefilled_refs = "\n".join([p['ref_code'] for p in st.session_state.edit_data['parcels']])
            prefilled_rider = st.session_state.edit_data['rider']

        ref_codes_text = st.text_area(
            "🏷️ รหัสอ้างอิง (รองรับทุกรูปแบบ)",
            value=prefilled_refs,
            height=120,
            placeholder="วาง/พิมพ์รหัสอ้างอิง เช่น:\n1234 5678\n2ABC, 3DEF\n4GHI\t5JKL"
        )
        
        rider_name = st.text_input(
            "👤 ชื่อผู้รับผิดชอบ/ไรเดอร์", 
            value=prefilled_rider,
            placeholder="ใส่ชื่อไรเดอร์หรือผู้รับผิดชอบ"
        )

    with col2:
        st.subheader("⚡ ควบคุมเทพ")
        
        queue_input = st.number_input(
            "🎯 เลขคิว",
            value=st.session_state.edit_data['queue'] if st.session_state.edit_data else st.session_state.queue_number,
            min_value=1,
            step=1
        )
        
        st.markdown("---")
        
        # Quick preview
        if ref_codes_text.strip():
            parsed_codes = turbo_parse_refs(ref_codes_text)
            st.info(f"📋 พบรหัส: {len(parsed_codes)} รายการ")
            if len(parsed_codes) <= 5:
                st.caption(f"รหัส: {', '.join(parsed_codes)}")
        
        st.markdown("---")
        
        # Ultra action buttons
        if st.button("🚀 สร้างใบจัดสินค้า!", key="create_btn", use_container_width=True):
            if not ref_codes_text.strip() or not rider_name.strip():
                st.error("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
            else:
                parsed_codes = turbo_parse_refs(ref_codes_text)
                if not parsed_codes:
                    st.error("⚠️ ไม่พบรหัสอ้างอิงที่ถูกต้อง")
                else:
                    # Ultra-fast processing
                    parcels = [{"ref_code": code} for code in parsed_codes]
                    sorted_parcels = lightning_sort(parcels)
                    
                    new_picklist = {
                        "queue": queue_input,
                        "rider": rider_name.strip(),
                        "parcels": sorted_parcels,
                        "time": datetime.now().strftime('%H:%M:%S'),
                        "date": datetime.now().strftime('%d/%m/%Y'),
                        "items_count": len(sorted_parcels)
                    }
                    
                    # Handle edit vs new
                    if st.session_state.edit_data:
                        # Update existing
                        for i, p in enumerate(st.session_state.completed_picklists):
                            if p['queue'] == st.session_state.edit_data['queue']:
                                st.session_state.completed_picklists[i] = new_picklist
                                break
                        st.session_state.edit_data = None
                        success_msg = f"✅ อัปเดตใบจัดสินค้า #{queue_input} เรียบร้อย"
                    else:
                        # Add new
                        st.session_state.completed_picklists.insert(0, new_picklist)
                        success_msg = f"✅ สร้างใบจัดสินค้า #{queue_input} เรียบร้อย"
                    
                    # Update queue number
                    st.session_state.queue_number = max([p['queue'] for p in st.session_state.completed_picklists] + [0]) + 1
                    st.session_state.last_rider_name = rider_name.strip()
                    
                    st.markdown(f'<div class="success-message">{success_msg}</div>', unsafe_allow_html=True)
                    st.balloons()
                    st.rerun()
        
        col_clear, col_bulk = st.columns(2)
        with col_clear:
            if st.button("🗑️ ล้าง", use_container_width=True):
                st.session_state.edit_data = None
                st.rerun()
        
        with col_bulk:
            if st.button("📁 นำเข้า", use_container_width=True, help="นำเข้าจากไฟล์ CSV"):
                st.info("🚧 ฟีเจอร์นี้กำลังพัฒนา")

    st.divider()

    # --- ULTRA PICKLIST DISPLAY ---
    st.subheader("📋 รายการที่สร้างแล้ว")
    
    if not st.session_state.completed_picklists:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #f5f7fa, #c3cfe2); border-radius: 15px; margin: 20px 0;">
            <h3 style="color: #667eea; margin-bottom: 10px;">🎯 ยังไม่มีใบจัดสินค้าในระบบ</h3>
            <p style="color: #666; font-size: 16px;">เริ่มต้นสร้างใบจัดสินค้าแรกของคุณเลย!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Quick filter and sort
        col_filter, col_sort = st.columns([3, 1])
        with col_filter:
            search_term = st.text_input("🔍 ค้นหารายการ", placeholder="ค้นหาด้วยชื่อไรเดอร์หรือรหัส...")
        with col_sort:
            sort_option = st.selectbox("📊 เรียงตาม", ["คิวล่าสุด", "คิวเก่าสุด", "ชื่อไรเดอร์", "จำนวนรายการ"])
        
        # Filter and sort logic
        filtered_picklists = st.session_state.completed_picklists
        if search_term:
            filtered_picklists = [
                p for p in filtered_picklists 
                if search_term.lower() in p['rider'].lower() or 
                   any(search_term.upper() in item['ref_code'] for item in p['parcels'])
            ]
        
        # Sorting
        if sort_option == "คิวล่าสุด":
            sorted_picklists = sorted(filtered_picklists, key=lambda x: x['queue'], reverse=True)
        elif sort_option == "คิวเก่าสุด":
            sorted_picklists = sorted(filtered_picklists, key=lambda x: x['queue'])
        elif sort_option == "ชื่อไรเดอร์":
            sorted_picklists = sorted(filtered_picklists, key=lambda x: x['rider'])
        else:  # จำนวนรายการ
            sorted_picklists = sorted(filtered_picklists, key=lambda x: len(x['parcels']), reverse=True)
        
        # Display with better performance
        for i, picklist in enumerate(sorted_picklists[:50]):  # Limit display for performance
            with st.container():
                st.markdown(f'<div class="picklist-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([5, 2, 2])
                
                with col1:
                    st.markdown(f'<span class="queue-badge">#{picklist["queue"]}</span> **{picklist["rider"]}**', unsafe_allow_html=True)
                    
                    codes = [p['ref_code'] for p in picklist['parcels']]
                    if len(codes) <= 10:
                        st.caption(f"📦 รายการ: {', '.join(codes)}")
                    else:
                        st.caption(f"📦 รายการ: {', '.join(codes[:10])}... (+{len(codes)-10})")
                
                with col2:
                    st.markdown(f'<span class="count-badge">{len(picklist["parcels"])} ชิ้น</span>', unsafe_allow_html=True)
                    st.caption(f"⏰ {picklist['time']}")
                
                with col3:
                    # Action buttons
                    col_print, col_edit, col_delete = st.columns(3)
                    
                    with col_print:
                        html_content = generate_ultra_html(picklist['rider'], picklist['queue'], picklist['parcels'])
                        st.download_button(
                            label="🖨️",
                            data=html_content,
                            file_name=f"picklist_Q{picklist['queue']}.html",
                            mime="text/html",
                            key=f"print_{picklist['queue']}_{i}",
                            use_container_width=True,
                            help="พิมพ์ใบจัดสินค้า"
                        )
                    
                    with col_edit:
                        if st.button("✏️", key=f"edit_{picklist['queue']}_{i}", use_container_width=True, help="แก้ไข"):
                            st.session_state.edit_data = picklist
                            st.rerun()
                    
                    with col_delete:
                        if st.button("🗑️", key=f"delete_{picklist['queue']}_{i}", use_container_width=True, help="ลบ"):
                            st.session_state.completed_picklists = [
                                p for p in st.session_state.completed_picklists 
                                if p['queue'] != picklist['queue']
                            ]
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Show pagination info if truncated
        if len(sorted_picklists) > 50:
            st.info(f"🔍 แสดง 50 รายการจากทั้งหมด {len(sorted_picklists)} รายการ")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "⚡ ระบบจัดทำใบจัดสินค้าเทพ - เร็ว แม่น เทพ 🚀"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()