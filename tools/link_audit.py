from pathlib import Path
import subprocess,sys,shutil,json
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);out.mkdir(parents=True)
lib=out/'Build/Online/libmugoat_online.a';lib.parent.mkdir(parents=True);shutil.copyfile(root/'network/native-port/online-bridge/target/aarch64-apple-ios/release/libmugoat_online.a',lib)
(out/'host.c').write_text('''#include "MugoatOnline.h"
int mugoat_command_info(const char*n,uint32_t*p,uint32_t c,uint32_t*r){return -1;}
bool mugoat_command_call(void*i,const char*n,const MugoatValue*a,uint32_t c,MugoatValue*r){return false;}
uint8_t*mugoat_memory_data(void*i,uint64_t*s){*s=0;return NULL;}
int main(void){char status[512];MugoatOnlineConfigure("127.0.0.1:47520","Audit","roleplay",2);mugoat_script_tick(NULL,0,0);mugoat_explosion(0);mugoat_time_warp(0);MugoatOnlineStatus(status,512);return MugoatOnlineConnected()?0:1;}
''')
sdk=subprocess.check_output(['xcrun','--sdk','iphoneos','--show-sdk-path'],text=True).strip()
r=subprocess.run(['xcrun','clang','-target','arm64-apple-ios16.0','-isysroot',sdk,'-I',str(root/'app/Source'),str(out/'host.c'),str(lib),'-o',str(out/'direct-link')],text=True,capture_output=True)
print('FULL-PATH DIRECT LINK exit',r.returncode);print(r.stderr[-16000:])
for name,search in [('NoSearch',''),('WithSearch','    LIBRARY_SEARCH_PATHS: "$(inherited) $(SRCROOT)/Build/Online"\n')]:
 spec='''name: LinkAudit
options:
  deploymentTarget:
    iOS: "16.0"
settings:
  base:
    HEADER_SEARCH_PATHS: "HEADERPATH"
    GENERATE_INFOPLIST_FILE: YES
SEARCHtargets:
  LinkAudit:
    type: application
    platform: iOS
    sources: [host.c]
    dependencies:
      - framework: Build/Online/libmugoat_online.a
        embed: false
      - sdk: UIKit.framework
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: vn.gta.link.audit
'''.replace('HEADERPATH',str(root/'app/Source')).replace('SEARCH',search)
 (out/'project.yml').write_text(spec)
 subprocess.run(['xcodegen','generate','--spec','project.yml'],cwd=out,check=True)
 p=subprocess.run(['xcodebuild','-project','LinkAudit.xcodeproj','-scheme','LinkAudit','-configuration','Release','-sdk','iphoneos','-derivedDataPath',str(out/name),'CODE_SIGNING_ALLOWED=NO','build'],cwd=out,text=True,capture_output=True)
 log=p.stdout+p.stderr;(out/(name+'.log')).write_text(log)
 lines=log.splitlines();print('XCODE AUDIT',name,'exit',p.returncode)
 for i,line in enumerate(lines):
  if any(x in line for x in ['Undefined symbols','ld:','error:','not found','BUILD SUCCEEDED']):print('\n'.join(lines[max(0,i-1):min(len(lines),i+25)]))
