项目根目录/
├── CLAUDE.md                           # 根入口，包含"内容探索"， 项目小直接指向蓝图， 项目大则指向代码内部.md  
├── .blueprint/
│   src/
    ├── auth/
    │   └── auth.service.md
    └── api/
        └── api.controller.md
└── src/
    ├── auth/
    │   /auth-module.md             介绍模块功能，然后指明熟悉代码请从蓝图开始，指向  .blueprint/  src/  auth/
    │   └── auth.service.ts
    └── api/
     /api-design.md 介绍模块功能，然后指明熟悉代码请从蓝图开始，指向  .blueprint/  src/  api/
        └── api.controller.ts
