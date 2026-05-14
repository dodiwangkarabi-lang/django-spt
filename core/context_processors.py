from core.permissions.roles import is_kasubag, is_pegawai, is_pimpinan

def app_permission(request):
    user = request.user
    
    return {
        "is_pegawai": is_pegawai(user),
        "is_kasubag": is_kasubag(user),
        "is_pimpinan": is_pimpinan(user)
    }

def sidebar_menu(request):
    user = request.user
    
    kasubag = user.groups.filter(name="kasubag").exists()
    pimpinan = user.groups.filter(name="pimpinan").exists()
    pegawai = user.groups.filter(name="pegawai").exists()
    
    menu = []

    if pegawai:
        menu += [
            {"url": "core_pegawai_dashboard", "label": "🏠 Dashboard"},
            # {"url": "core_permohonan_spt", "label": "📄 Permohonan"},
            {"url": "core_spt_diterima", "label": "📄 SPT diterima"},
            {"url": "core_ajukan_spt", "label": "➕ Ajukan Permohonan"},
        ]
    elif kasubag:
        menu += [
            {"url": "core_kasubag_dashboard", "label": "🏠 Dashboard"},
            {"url": "core_kasubag_disposisi", "label": "📄 Daftar Masuk"},
            {"url": "spt_list", "label": "📄 Daftar SPT"},
            # {"url": "disposisi_list", "label": "📄 Daftar Disposisi"},
            
        ]
    elif pimpinan:
        menu += [
            {"url": "core_pimpinan_dashboard", "label": "🏠 Dashboard"},
            {"url": "core_pimpinan_disposisi", "label": "📄 Daftar Masuk"},
            {"url": "core_pimpinan_laporan_pelaksanaan", "label": "📄 Laporan Pelaksanaan"},
            {"url": "spt_list", "label": "📄 Daftar SPT"},
            # {"url": "disposisi_list", "label": "📄 Daftar Disposisi"},
        ]

    # shared menu
    menu += [
        {"label": "📄 Permohonan", "url": "permohonan_list"},
    ]

    return {"sidebar_menu": menu}