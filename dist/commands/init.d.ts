/**
 * Init Command
 * 初始化 bwflow 结构到用户项目
 */
interface InitOptions {
    type?: string;
    user?: string;
    yes?: boolean;
    force?: boolean;
}
/**
 * 初始化 bwflow 结构
 */
export declare function initCommand(options: InitOptions): Promise<void>;
export {};
