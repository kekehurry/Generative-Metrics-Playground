import BigNumber from 'bignumber.js';

// 高精度计算的处理函数集合
const bignumberFc = {
  add: (a: number, b: number) => {
    return new BigNumber(a).plus(b).toNumber();
  },
  subtract: (a: number, b: number) => {
    return new BigNumber(a).minus(b).toNumber();
  },
  multiply: (a: number, b: number) => {
    return new BigNumber(a).multipliedBy(b).toNumber();
  },
  divide: (a: number, b: number) => {
    return new BigNumber(a).dividedBy(b).toNumber();
  },
  // 均值
  avg: (arr: number[]) => {
    let total: number = 0;
    for (let i: number = 0; i < arr.length; i++) {
      total = bignumberFc.add(total, arr[i]);
    }
    return bignumberFc.divide(total, arr.length);
  },
  // 方差
  variance: (arr: number[]) => {
    let total: number = 0;
    for (let i: number = 0; i < arr.length; i++) {
      total = bignumberFc.add(total, arr[i]);
    }

    const mean = bignumberFc.divide(total, arr.length);

    let totalS: number = 0;
    for (let i: number = 0; i < arr.length; i++) {
      const tempEverySubtract: number = bignumberFc.subtract(arr[i], mean);
      totalS = bignumberFc.add(totalS, bignumberFc.multiply(tempEverySubtract, tempEverySubtract));
    }
    return bignumberFc.divide(totalS, arr.length);
  },
  //  线性回归
  regression: (list: any[]) => {
    if (!list) return '';
    if (list.length === 0) return '';

    //  x，y总数
    let totalX: number = 0,
      totalY: number = 0;
    //  x，y平均数
    let avgX: number = 0,
      avgY: number = 0;
    //  数组长度
    let n: number = list?.length;
    //  xy阶乘
    let xy2: number = 0;
    //  x平方阶乘
    let x2: number = 0;
    //  斜率b，常量a
    let b: number = 0,
      a: number = 0;
    //  分子、分母
    let fz: number = 0,
      fm: number = 0;
    //  回归线
    let fn: string = '';

    for (let i = 0; i < n; i++) {
      totalX += list[i][0];
      totalY += list[i][1];
      xy2 += bignumberFc.multiply(list[i][0], list[i][1]);
      x2 += bignumberFc.multiply(list[i][0], list[i][0]);
    }

    //  均值
    avgX = bignumberFc.divide(totalX, n);
    avgY = bignumberFc.divide(totalY, n);

    //  分子分母
    let nxy = bignumberFc.multiply(n, bignumberFc.multiply(avgX, avgY));
    fz = bignumberFc.subtract(xy2, nxy);
    let nx = bignumberFc.multiply(n, bignumberFc.multiply(avgX, avgX));
    fm = bignumberFc.subtract(x2, nx);

    b = bignumberFc.divide(fz, fm);
    a = bignumberFc.subtract(list[0][1], bignumberFc.multiply(b, list[0][0]));

    fn = a < 0 ? 'y=' + (b == 0 ? '' : b + 'x') + a : 'y=' + (b == 0 ? '' : b + 'x+') + a;

    return fn;

    // console.log(avgX,'平均数x');
    // console.log(avgY,'平均数y');
    // console.log(nxy,'nxy');
    // console.log(nx,'nx');
    // console.log(fz,'分子');
    // console.log(x2,'x2');
    // console.log(xy2,'xy2');
    // console.log(fm,'分母');
    // console.log(fn,'线性回归方程');
  },
};